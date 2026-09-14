#!/usr/bin/env python3
"""Validate a withheld-truth RightsLedger blind-test bundle with stdlib only."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path


CASE_IDS = tuple(f"B{index:02d}" for index in range(1, 6))
ORIGIN_TYPES = {"third_party_free", "purchased", "open_source", "ai_generated", "original", "output"}
EVIDENCE_TYPES = {"source", "license", "receipt", "prompt", "model_terms", "author"}
RELATION_TYPES = {"ingredient", *(f"evidence:{kind}" for kind in EVIDENCE_TYPES)}
CHALLENGE_TAGS = {
    "renamed_asset",
    "ambiguous_candidate",
    "unrelated_evidence",
    "missing_evidence",
    "multilingual_clue",
    "c2pa",
}
SPIKE_SAMPLE_HASHES = {
    "f999fd78bfe8a83c96e468a078830ba94485bc1bc6fd086fb94a43bd29dd0f23",
    "75a8da33f6eaf1e16bf3b42cd78913b22b2e6a671fda217a508b1ba4230ce864",
    "0d4c2774f1b7e94b9613bb952b0a76b6a178d22ac6d206d257d2af1376cbbff2",
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac"}
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".css", ".html", ".svelte"}


class IntakeError(Exception):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing file: {path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        errors.append(f"invalid JSON: {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"JSON root must be an object: {path}")
        return {}
    return value


def safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts and value == path.as_posix()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(sha256(path).encode())
        digest.update(b"\0")
    return digest.hexdigest()


def modality(path: str) -> str | None:
    suffix = Path(path).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    if suffix in CODE_EXTENSIONS:
        return "code"
    return None


def validate_bundle(root: Path) -> dict:
    errors: list[str] = []
    all_tags: set[str] = set()
    project_types: set[str] = set()
    modalities: set[str] = set()
    total_primary = total_missing = total_c2pa = 0
    case_receipts = []

    for case_id in CASE_IDS:
        project = root / "projects" / case_id / "project"
        shared_path = root / "shared" / f"{case_id}.json"
        truth_path = root / "truth" / f"{case_id}.json"
        if not project.is_dir():
            errors.append(f"missing project directory: {project}")
        if project.exists() and any(path.is_symlink() for path in project.rglob("*")):
            errors.append(f"symlink not allowed in project: {case_id}")

        shared = load_json(shared_path, errors)
        truth = load_json(truth_path, errors)
        if shared.get("schema_version") != "2.0" or truth.get("schema_version") != "2.0":
            errors.append(f"{case_id}: schema_version must be 2.0")
        if shared.get("case_id") != case_id or truth.get("case_id") != case_id:
            errors.append(f"{case_id}: case_id mismatch")
        if set(shared) - {"schema_version", "case_id", "project_type", "subjects"}:
            errors.append(f"{case_id}: shared manifest contains unapproved fields")

        project_type = shared.get("project_type")
        if not isinstance(project_type, str) or not project_type.strip() or project_type.startswith("replace_"):
            errors.append(f"{case_id}: project_type is not filled")
        else:
            project_types.add(project_type.strip().lower())

        subjects = shared.get("subjects", [])
        if not isinstance(subjects, list):
            errors.append(f"{case_id}: subjects must be a list")
            subjects = []
        subject_paths: dict[str, str] = {}
        for index, subject in enumerate(subjects):
            if not isinstance(subject, dict) or set(subject) != {"path", "description", "origin_type"}:
                errors.append(f"{case_id}: invalid subject fields at index {index}")
                continue
            path = subject.get("path")
            description = subject.get("description")
            origin = subject.get("origin_type")
            if not safe_relative(path):
                errors.append(f"{case_id}: unsafe subject path: {path}")
                continue
            if path in subject_paths:
                errors.append(f"{case_id}: duplicate subject path: {path}")
            subject_paths[path] = origin
            if origin not in ORIGIN_TYPES:
                errors.append(f"{case_id}: invalid origin_type for {path}")
            if not isinstance(description, str) or not description.strip() or description.startswith("neutral description"):
                errors.append(f"{case_id}: missing neutral description for {path}")
            if project.is_dir() and not (project / path).is_file():
                errors.append(f"{case_id}: subject file missing: {path}")
            if origin != "output" and (kind := modality(path)):
                modalities.add(kind)

        primary = {path for path, origin in subject_paths.items() if origin != "output"}
        outputs = {path for path, origin in subject_paths.items() if origin == "output"}
        total_primary += len(primary)
        if len(primary) != 15:
            errors.append(f"{case_id}: expected 15 primary assets, found {len(primary)}")
        if not outputs:
            errors.append(f"{case_id}: at least one output is required")

        author = truth.get("created_by")
        if not isinstance(author, str) or len(author.strip()) < 3 or "pseudonym" in author:
            errors.append(f"{case_id}: independent author pseudonym is not filled")
        if truth.get("sealed_until") != "all_ten_review_submissions_hashed":
            errors.append(f"{case_id}: sealed_until is invalid")

        tags = truth.get("challenge_tags", [])
        if not isinstance(tags, list) or len(set(tags)) < 2 or not set(tags) <= CHALLENGE_TAGS:
            errors.append(f"{case_id}: use at least two allowed challenge_tags")
        else:
            all_tags.update(tags)

        actual_files = {
            path.relative_to(project).as_posix()
            for path in project.rglob("*")
            if path.is_file()
        } if project.is_dir() else set()
        relations = truth.get("relations", [])
        if not isinstance(relations, list) or not relations:
            errors.append(f"{case_id}: relations must be a non-empty list")
            relations = []
        seen_relations = set()
        for relation in relations:
            if not isinstance(relation, dict):
                errors.append(f"{case_id}: invalid relation object")
                continue
            key = (relation.get("relation_type"), relation.get("from"), relation.get("to"))
            if key in seen_relations:
                errors.append(f"{case_id}: duplicate relation: {key}")
            seen_relations.add(key)
            relation_type, source, target = key
            if relation_type not in RELATION_TYPES or not safe_relative(source) or not safe_relative(target):
                errors.append(f"{case_id}: invalid relation: {key}")
                continue
            if source not in actual_files or target not in actual_files:
                errors.append(f"{case_id}: relation path missing: {key}")
            if relation_type == "ingredient" and (source not in outputs or target not in primary):
                errors.append(f"{case_id}: ingredient must link output to primary asset: {key}")
            if relation_type.startswith("evidence:") and source not in primary:
                errors.append(f"{case_id}: evidence must originate from primary asset: {key}")

        missing = truth.get("missing_evidence", [])
        if not isinstance(missing, list):
            errors.append(f"{case_id}: missing_evidence must be a list")
            missing = []
        missing_keys = set()
        for item in missing:
            if not isinstance(item, dict):
                errors.append(f"{case_id}: invalid missing_evidence object")
                continue
            key = (item.get("asset"), item.get("evidence_type"))
            missing_keys.add(key)
            if key[0] not in primary or key[1] not in EVIDENCE_TYPES:
                errors.append(f"{case_id}: invalid missing evidence: {key}")
        if len(missing_keys) != len(missing):
            errors.append(f"{case_id}: duplicate missing_evidence rows")
        if len(missing_keys) < 2:
            errors.append(f"{case_id}: at least two missing evidence truths are required")
        total_missing += len(missing_keys)

        c2pa_rows = truth.get("c2pa_expected", [])
        if not isinstance(c2pa_rows, list):
            errors.append(f"{case_id}: c2pa_expected must be a list")
            c2pa_rows = []
        for item in c2pa_rows:
            asset = item.get("asset") if isinstance(item, dict) else None
            report = item.get("validation_report") if isinstance(item, dict) else None
            if asset not in primary or not safe_relative(report) or not (root / report).is_file():
                errors.append(f"{case_id}: invalid C2PA asset or report")
                continue
            if sha256(project / asset) in SPIKE_SAMPLE_HASHES:
                errors.append(f"{case_id}: C2PA spike sample reuse is forbidden")
            if item.get("manifest_presence") not in {"present", "absent"}:
                errors.append(f"{case_id}: invalid C2PA manifest_presence")
            if item.get("integrity_state") not in {"valid", "invalid", "not_applicable"}:
                errors.append(f"{case_id}: invalid C2PA integrity_state")
            if item.get("signer_trust_state") not in {"untrusted", "not_reported_untrusted", "not_applicable"}:
                errors.append(f"{case_id}: invalid C2PA signer_trust_state")
            total_c2pa += 1

        if shared_path.is_file() and truth_path.is_file() and project.is_dir():
            case_receipts.append(
                {
                    "case_id": case_id,
                    "project_tree_sha256": tree_sha256(project),
                    "shared_sha256": sha256(shared_path),
                    "truth_sha256": sha256(truth_path),
                    "primary_asset_count": len(primary),
                    "missing_evidence_count": len(missing_keys),
                }
            )

    if len(project_types) < 4:
        errors.append(f"expected at least four distinct project types, found {len(project_types)}")
    if not {"image", "audio", "code"} <= modalities:
        errors.append(f"dataset must include image, audio, and code assets; found {sorted(modalities)}")
    if all_tags != CHALLENGE_TAGS:
        errors.append(f"challenge tag coverage mismatch; missing {sorted(CHALLENGE_TAGS - all_tags)}")
    if total_primary != 75:
        errors.append(f"expected 75 primary assets, found {total_primary}")
    if total_missing < 10:
        errors.append(f"expected at least 10 missing evidence truths, found {total_missing}")
    if total_c2pa < 1:
        errors.append("at least one held-out C2PA truth is required")
    if errors:
        raise IntakeError("\n".join(errors))

    return {
        "schema_version": "2.0",
        "validated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "validator_sha256": sha256(Path(__file__)),
        "all_checks_passed": True,
        "case_count": len(CASE_IDS),
        "primary_asset_count": total_primary,
        "missing_evidence_count": total_missing,
        "held_out_c2pa_count": total_c2pa,
        "distinct_project_type_count": len(project_types),
        "modalities": sorted(modalities),
        "challenge_tags": sorted(all_tags),
        "cases": case_receipts,
        "truth_release_rule": "withhold truth until all ten review submissions are hashed",
    }


def self_check() -> None:
    tag_sets = (
        ["renamed_asset", "c2pa"],
        ["ambiguous_candidate", "missing_evidence"],
        ["unrelated_evidence", "multilingual_clue"],
        ["renamed_asset", "ambiguous_candidate"],
        ["missing_evidence", "multilingual_clue"],
    )
    extensions = (".png", ".wav", ".js")
    origins = ("third_party_free", "purchased", "open_source", "ai_generated", "original")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for case_index, case_id in enumerate(CASE_IDS):
            project = root / "projects" / case_id / "project"
            subjects = []
            for asset_index in range(15):
                suffix = extensions[asset_index] if asset_index < 3 else ".txt"
                relative = f"assets/asset_{asset_index + 1:02d}{suffix}"
                path = project / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"test asset {asset_index}\n", encoding="utf-8")
                subjects.append(
                    {
                        "path": relative,
                        "description": f"neutral test asset {asset_index + 1}",
                        "origin_type": origins[asset_index % len(origins)],
                    }
                )
            output = project / "deliverables/output.txt"
            evidence = project / "evidence/source.txt"
            output.parent.mkdir(parents=True, exist_ok=True)
            evidence.parent.mkdir(parents=True, exist_ok=True)
            output.write_text("test output\n", encoding="utf-8")
            evidence.write_text("test source\n", encoding="utf-8")
            subjects.append({"path": "deliverables/output.txt", "description": "neutral test output", "origin_type": "output"})
            write_json(
                root / "shared" / f"{case_id}.json",
                {"schema_version": "2.0", "case_id": case_id, "project_type": f"test-type-{case_index}", "subjects": subjects},
            )
            c2pa = []
            if case_id == "B01":
                report = root / "truth" / "c2pa" / "B01.json"
                write_json(report, {"test": True})
                c2pa = [
                    {
                        "asset": "assets/asset_01.png",
                        "manifest_presence": "present",
                        "integrity_state": "valid",
                        "signer_trust_state": "not_reported_untrusted",
                        "validation_report": "truth/c2pa/B01.json",
                    }
                ]
            write_json(
                root / "truth" / f"{case_id}.json",
                {
                    "schema_version": "2.0",
                    "case_id": case_id,
                    "created_by": "independent-test-author",
                    "challenge_tags": tag_sets[case_index],
                    "relations": [
                        {"relation_type": "ingredient", "from": "deliverables/output.txt", "to": "assets/asset_01.png"},
                        {"relation_type": "evidence:source", "from": "assets/asset_01.png", "to": "evidence/source.txt"},
                    ],
                    "missing_evidence": [
                        {"asset": "assets/asset_02.wav", "evidence_type": "receipt"},
                        {"asset": "assets/asset_03.js", "evidence_type": "license"},
                    ],
                    "c2pa_expected": c2pa,
                    "sealed_until": "all_ten_review_submissions_hashed",
                },
            )
        receipt = validate_bundle(root)
        assert receipt["primary_asset_count"] == 75
        assert receipt["missing_evidence_count"] == 10
        shared_path = root / "shared" / "B01.json"
        shared = json.loads(shared_path.read_text(encoding="utf-8"))
        shared["relations"] = []
        write_json(shared_path, shared)
        try:
            validate_bundle(root)
        except IntakeError:
            pass
        else:
            raise AssertionError("forbidden shared truth field was not rejected")
    print("PASS: valid bundle accepted and shared truth leakage rejected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.root is None:
        parser.error("root is required unless --self-check is used")
    try:
        receipt = validate_bundle(args.root.resolve())
    except IntakeError as exc:
        print(f"FAIL:\n{exc}", file=sys.stderr)
        raise SystemExit(1)
    if args.receipt:
        write_json(args.receipt, receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
