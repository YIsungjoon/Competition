#!/usr/bin/env python3
"""Local, dependency-free RightsLedger MVP server."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
APP_VERSION = "0.1.0"
OBSERVATIONS = ".rightsledger_observations.json"
MODEL = os.environ.get("RIGHTSLEDGER_EMBED_MODEL", "bge-m3:latest")
DEFAULT_OLLAMA_URL = os.environ.get("RIGHTSLEDGER_OLLAMA_URL", "http://127.0.0.1:11434")
MIN_SIMILARITY = 0.58
MIN_MARGIN = 0.025
MAX_FILES = 200
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_BYTES = 25 * 1024 * 1024
MAX_REQUEST_BYTES = 40 * 1024 * 1024
MAX_TEXT_CHARS = 20_000
C2PA_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mov"}
REQUIREMENTS = {
    "third_party_free": {"source", "license"},
    "purchased": {"receipt", "license"},
    "open_source": {"source", "license"},
    "ai_generated": {"prompt", "model_terms"},
    "original": {"author"},
    "output": set(),
}


class APIError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


def utc_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_parts(raw: object) -> tuple[str, ...]:
    if not isinstance(raw, str) or not raw or "\x00" in raw:
        raise APIError(400, "파일 경로가 비어 있거나 올바르지 않습니다.")
    clean = raw.replace("\\", "/")
    if clean.startswith("/") or re.match(r"^[A-Za-z]:/", clean):
        raise APIError(400, f"절대 경로는 허용하지 않습니다: {raw}")
    parts = tuple(clean.split("/"))
    if any(part in {"", ".", ".."} for part in parts):
        raise APIError(400, f"안전하지 않은 파일 경로입니다: {raw}")
    return parts


def decode_upload(records: object) -> dict[str, bytes]:
    if not isinstance(records, list) or not records:
        raise APIError(400, "불러올 파일이 없습니다.")
    if len(records) > MAX_FILES:
        raise APIError(413, f"파일은 최대 {MAX_FILES}개까지 불러올 수 있습니다.")

    raw_items: list[tuple[tuple[str, ...], bytes]] = []
    total = 0
    for record in records:
        if not isinstance(record, dict):
            raise APIError(400, "파일 항목 형식이 올바르지 않습니다.")
        parts = safe_parts(record.get("path"))
        encoded = record.get("content_base64")
        if not isinstance(encoded, str):
            raise APIError(400, f"파일 내용이 없습니다: {'/'.join(parts)}")
        try:
            data = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise APIError(400, f"파일 인코딩이 올바르지 않습니다: {'/'.join(parts)}") from exc
        if len(data) > MAX_FILE_BYTES:
            raise APIError(413, f"파일 하나의 최대 크기는 5MB입니다: {'/'.join(parts)}")
        total += len(data)
        if total > MAX_TOTAL_BYTES:
            raise APIError(413, "전체 파일 크기는 최대 25MB입니다.")
        raw_items.append((parts, data))

    first = raw_items[0][0][0]
    strip_root = all(len(parts) > 1 and parts[0] == first for parts, _ in raw_items)
    decoded: dict[str, bytes] = {}
    for parts, data in raw_items:
        relative = "/".join(parts[1:] if strip_root else parts)
        safe_parts(relative)
        if relative in decoded:
            raise APIError(400, f"중복된 파일 경로입니다: {relative}")
        decoded[relative] = data
    return decoded


def parse_manifest(files: dict[str, bytes]) -> list[dict]:
    if OBSERVATIONS not in files:
        raise APIError(
            422,
            f"선택한 폴더의 최상위에 {OBSERVATIONS} 파일이 필요합니다.",
        )
    try:
        manifest = json.loads(files[OBSERVATIONS].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise APIError(422, f"{OBSERVATIONS}의 JSON 형식이 올바르지 않습니다.") from exc
    subjects = manifest.get("subjects") if isinstance(manifest, dict) else None
    if not isinstance(subjects, list) or not subjects:
        raise APIError(422, f"{OBSERVATIONS}에 비어 있지 않은 subjects 배열이 필요합니다.")

    cleaned = []
    seen = set()
    for index, item in enumerate(subjects, start=1):
        if not isinstance(item, dict):
            raise APIError(422, f"subjects[{index}]가 객체가 아닙니다.")
        path = "/".join(safe_parts(item.get("path")))
        description = item.get("description")
        origin_type = item.get("origin_type")
        if path == OBSERVATIONS or path not in files:
            raise APIError(422, f"선언한 자산 파일이 폴더에 없습니다: {path}")
        if path in seen:
            raise APIError(422, f"중복 선언된 자산입니다: {path}")
        if not isinstance(description, str) or not description.strip():
            raise APIError(422, f"자산 설명이 비어 있습니다: {path}")
        if len(description) > 500:
            raise APIError(422, f"자산 설명은 500자 이하여야 합니다: {path}")
        if origin_type not in REQUIREMENTS:
            allowed = ", ".join(REQUIREMENTS)
            raise APIError(422, f"지원하지 않는 취득 유형입니다: {origin_type}. 허용값: {allowed}")
        seen.add(path)
        cleaned.append(
            {"path": path, "description": description.strip(), "origin_type": origin_type}
        )
    if not any(item["origin_type"] != "output" for item in cleaned):
        raise APIError(422, "감사할 입력 자산이 하나 이상 필요합니다.")
    return cleaned


def decode_text(data: bytes) -> tuple[str, bool]:
    text = data.decode("utf-8", errors="replace")
    return text[:MAX_TEXT_CHARS], len(text) > MAX_TEXT_CHARS


def exact_matches(text: str, subjects: list[dict]) -> list[str]:
    lowered = text.lower()
    matches = []
    for item in subjects:
        path = item["path"].lower()
        name = PurePosixPath(path).name
        if path in lowered or name in lowered:
            matches.append(item["path"])
    return matches


def cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norms = math.sqrt(sum(a * a for a in left) * sum(b * b for b in right))
    return dot / norms if norms else 0.0


def asset_doc(item: dict) -> str:
    return f"Asset description: {item['description']}. Declared origin: {item['origin_type']}."


class OllamaEmbedder:
    def __init__(self, base_url: str):
        self.url = base_url.rstrip("/") + "/api/embed"
        self.cache: dict[str, list[float]] = {}

    def prepare(self, texts: list[str]) -> None:
        missing = list(dict.fromkeys(text for text in texts if text not in self.cache))
        if not missing:
            return
        body = json.dumps({"model": MODEL, "input": missing}).encode()
        request = urllib.request.Request(
            self.url, data=body, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = json.load(response)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise APIError(
                503,
                f"로컬 AI 모델에 연결하지 못했습니다. Ollama와 {MODEL}을 확인해 주세요.",
            ) from exc
        vectors = payload.get("embeddings", [])
        if len(vectors) != len(missing):
            raise APIError(503, "로컬 AI 모델이 예상한 수의 임베딩을 반환하지 않았습니다.")
        self.cache.update(zip(missing, vectors))

    def get(self, text: str) -> list[float]:
        return self.cache[text]


def semantic_scores(clue: str, candidates: list[dict], embedder: OllamaEmbedder) -> list[dict]:
    return sorted(
        (
            {
                "asset": item["path"],
                "score": round(cosine(embedder.get(clue), embedder.get(asset_doc(item))), 6),
            }
            for item in candidates
        ),
        key=lambda item: item["score"],
        reverse=True,
    )


def relation_from_task(task: dict, asset: str, method: str, scores: list[dict]) -> dict:
    if task["direction"] == "evidence":
        source, target = asset, task["endpoint"]
    else:
        source, target = task["endpoint"], asset
    margin = None
    confidence = 1.0
    if method == "embedding":
        confidence = scores[0]["score"]
        margin = round(confidence - (scores[1]["score"] if len(scores) > 1 else 0.0), 6)
    return {
        "relation_type": task["relation_type"],
        "from": source,
        "to": target,
        "method": method,
        "confidence": confidence,
        "margin": margin,
        "candidates": scores[:3],
    }


def build_tasks(files: dict[str, bytes], subjects: list[dict]) -> tuple[list[dict], list[dict], list[str]]:
    inputs = [item for item in subjects if item["origin_type"] != "output"]
    outputs = [item for item in subjects if item["origin_type"] == "output"]
    tasks = []
    unresolved = []
    warnings = []

    for path in sorted(files):
        parts = PurePosixPath(path).parts
        if len(parts) < 3 or parts[0] != "evidence":
            continue
        kind = parts[1]
        if kind not in {value for values in REQUIREMENTS.values() for value in values}:
            warnings.append(f"지원하지 않는 증거 종류라 건너뜀: {path}")
            continue
        clue, truncated = decode_text(files[path])
        if truncated:
            warnings.append(f"처음 {MAX_TEXT_CHARS}자만 분석함: {path}")
        candidates = [item for item in inputs if kind in REQUIREMENTS[item["origin_type"]]]
        tasks.append(
            {
                "clue": clue.strip(),
                "clue_path": path,
                "relation_type": f"evidence:{kind}",
                "direction": "evidence",
                "endpoint": path,
                "candidates": candidates,
            }
        )

    for path in sorted(files):
        if not path.startswith("lineage/") or PurePosixPath(path).suffix.lower() not in {".md", ".txt"}:
            continue
        text, truncated = decode_text(files[path])
        if truncated:
            warnings.append(f"처음 {MAX_TEXT_CHARS}자만 분석함: {path}")
        lines = text.splitlines()
        output_lines = [line.split(":", 1)[1].strip() for line in lines if line.startswith("Output:")]
        output_matches = exact_matches(output_lines[0], outputs) if len(output_lines) == 1 else []
        if len(output_matches) != 1:
            unresolved.append(
                {
                    "clue": path,
                    "relation_type": "lineage_output",
                    "direction": "output",
                    "endpoint": None,
                    "reason": "결과물 경로를 하나로 확정하지 못함",
                    "candidates": [],
                }
            )
            continue
        for index, line in enumerate((line for line in lines if line.startswith("Ingredient:")), 1):
            clue = line.split(":", 1)[1].strip()
            tasks.append(
                {
                    "clue": clue,
                    "clue_path": f"{path}#ingredient-{index}",
                    "relation_type": "ingredient",
                    "direction": "ingredient",
                    "endpoint": output_matches[0],
                    "candidates": inputs,
                }
            )
    return tasks, unresolved, warnings


def missing_evidence(subjects: list[dict], relations: list[dict]) -> list[dict]:
    provided: dict[str, set[str]] = {}
    for relation in relations:
        if relation["relation_type"].startswith("evidence:"):
            provided.setdefault(relation["from"], set()).add(
                relation["relation_type"].split(":", 1)[1]
            )
    missing = []
    for item in subjects:
        if item["origin_type"] == "output":
            continue
        for kind in sorted(REQUIREMENTS[item["origin_type"]] - provided.get(item["path"], set())):
            missing.append({"asset": item["path"], "evidence_type": kind})
    return missing


def c2pa_codes(report: dict) -> list[str]:
    return sorted(
        {
            item.get("code")
            for item in report.get("validation_status", [])
            if isinstance(item, dict) and item.get("code")
        }
    )


def inspect_c2pa(path: str, data: bytes, executable: str | None) -> dict:
    result = {
        "path": path,
        "manifest_presence": "unknown",
        "integrity_state": "unknown",
        "signer_trust_state": "unknown",
        "validation_codes": [],
        "rights_permission_state": "not_evaluated",
    }
    if not executable:
        return {**result, "tool_state": "unavailable"}
    suffix = PurePosixPath(path).suffix.lower()
    with tempfile.TemporaryDirectory(prefix="rightsledger-c2pa-") as tmp:
        target = Path(tmp) / f"asset{suffix}"
        target.write_bytes(data)
        try:
            process = subprocess.run(
                [executable, str(target)], capture_output=True, text=True, timeout=15
            )
        except subprocess.TimeoutExpired:
            return {**result, "tool_state": "timeout"}
    combined = f"{process.stdout}\n{process.stderr}"
    if "No claim found" in combined:
        return {
            **result,
            "tool_state": "ok",
            "manifest_presence": "absent",
            "integrity_state": "not_applicable",
            "signer_trust_state": "not_applicable",
        }
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError:
        return {**result, "tool_state": "unsupported_or_unreadable"}

    codes = c2pa_codes(report)
    presence = "present" if report.get("active_manifest") else "absent"
    raw_state = report.get("validation_state")
    integrity = "valid" if raw_state == "Valid" else "invalid" if raw_state == "Invalid" else "unknown"
    trust = "untrusted" if "signingCredential.untrusted" in codes else "not_reported_untrusted"
    if presence == "absent":
        integrity, trust = "not_applicable", "not_applicable"
    return {
        **result,
        "tool_state": "ok",
        "manifest_presence": presence,
        "integrity_state": integrity,
        "signer_trust_state": trust,
        "validation_codes": codes,
    }


def analyze_project(files: dict[str, bytes], ollama_url: str, run_c2pa: bool = True) -> dict:
    subjects = parse_manifest(files)
    tasks, unresolved, warnings = build_tasks(files, subjects)
    relations = []
    semantic_tasks = []

    for task in tasks:
        exact = exact_matches(task["clue"], task["candidates"])
        if exact:
            for asset in exact:
                relations.append(
                    relation_from_task(task, asset, "exact", [{"asset": asset, "score": 1.0}])
                )
        elif task["candidates"]:
            semantic_tasks.append(task)
        else:
            unresolved.append(
                {
                    "clue": task["clue_path"],
                    "relation_type": task["relation_type"],
                    "direction": task["direction"],
                    "endpoint": task["endpoint"],
                    "reason": "해당 증거 종류를 요구하는 자산이 없음",
                    "candidates": [],
                }
            )

    if semantic_tasks:
        embedder = OllamaEmbedder(ollama_url)
        texts = [task["clue"] for task in semantic_tasks]
        texts.extend(asset_doc(item) for task in semantic_tasks for item in task["candidates"])
        embedder.prepare(texts)
        for task in semantic_tasks:
            scores = semantic_scores(task["clue"], task["candidates"], embedder)
            margin = scores[0]["score"] - (scores[1]["score"] if len(scores) > 1 else 0.0)
            if scores[0]["score"] >= MIN_SIMILARITY and margin >= MIN_MARGIN:
                relations.append(relation_from_task(task, scores[0]["asset"], "embedding", scores))
            else:
                unresolved.append(
                    {
                        "clue": task["clue_path"],
                        "relation_type": task["relation_type"],
                        "direction": task["direction"],
                        "endpoint": task["endpoint"],
                        "reason": "유사도 또는 1·2위 차이가 자동 연결 기준 미만",
                        "candidates": scores[:3],
                    }
                )

    unique = {}
    for relation in relations:
        key = relation["relation_type"], relation["from"], relation["to"]
        previous = unique.get(key)
        if previous is None or relation["method"] == "exact":
            unique[key] = relation
    relations = sorted(unique.values(), key=lambda item: (item["relation_type"], item["from"], item["to"]))
    for index, relation in enumerate(relations, 1):
        relation["id"] = f"REL-{index:03d}"

    inventory = [
        {
            "path": path,
            "size": len(data),
            "sha256": sha256_bytes(data),
            "declared_asset": any(item["path"] == path for item in subjects),
        }
        for path, data in sorted(files.items())
        if path != OBSERVATIONS
    ]
    c2pa_executable = shutil.which("c2patool") if run_c2pa else None
    c2pa = []
    if run_c2pa:
        for subject in subjects:
            path = subject["path"]
            if PurePosixPath(path).suffix.lower() in C2PA_SUFFIXES:
                c2pa.append(inspect_c2pa(path, files[path], c2pa_executable))

    return {
        "analysis_id": "RL-" + sha256_bytes(
            "".join(item["sha256"] for item in inventory).encode()
        )[:12],
        "generated_at": utc_now(),
        "app_version": APP_VERSION,
        "input_contract": OBSERVATIONS,
        "inventory": inventory,
        "subjects": subjects,
        "requirements": {key: sorted(value) for key, value in REQUIREMENTS.items()},
        "relations": relations,
        "missing_evidence": missing_evidence(subjects, relations),
        "unresolved": sorted(unresolved, key=lambda item: (item["relation_type"], item["clue"])),
        "c2pa": c2pa,
        "warnings": warnings,
        "ai": {
            "provider": "local_ollama",
            "model": MODEL,
            "semantic_tasks": len(semantic_tasks),
            "embedding_links": sum(item["method"] == "embedding" for item in relations),
            "deterministic_links": sum(item["method"] == "exact" for item in relations),
            "thresholds": {"min_similarity": MIN_SIMILARITY, "min_margin": MIN_MARGIN},
            "fallback_used": False,
        },
        "legal_conclusions": [],
        "interpretation_boundary": (
            "관계와 누락은 검토 후보이며 법률상 권리 보유 또는 제출 가능 결론이 아닙니다. "
            "C2PA 무결성·서명자 신뢰·권리 증거는 서로 다른 상태입니다."
        ),
    }


def service_health(ollama_url: str) -> dict:
    ollama = {"reachable": False, "model_available": False, "model": MODEL}
    try:
        with urllib.request.urlopen(ollama_url.rstrip("/") + "/api/tags", timeout=2) as response:
            payload = json.load(response)
        names = {item.get("name") for item in payload.get("models", [])}
        ollama = {"reachable": True, "model_available": MODEL in names, "model": MODEL}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        pass

    executable = shutil.which("c2patool")
    c2pa = {"available": bool(executable), "version": None}
    if executable:
        try:
            process = subprocess.run([executable, "-V"], capture_output=True, text=True, timeout=3)
            c2pa["version"] = (process.stdout or process.stderr).strip()
        except subprocess.TimeoutExpired:
            pass
    return {
        "status": "ready" if ollama["reachable"] and ollama["model_available"] else "needs_attention",
        "app_version": APP_VERSION,
        "ollama": ollama,
        "c2pa": c2pa,
        "persistence": "none",
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "RightsLedger/0.1"

    def send_bytes(self, status: int, content_type: str, data: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'")
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status: int, value: object) -> None:
        self.send_bytes(
            status,
            "application/json; charset=utf-8",
            (json.dumps(value, ensure_ascii=False) + "\n").encode(),
        )

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in {"/", "/index.html"}:
            self.send_bytes(200, "text/html; charset=utf-8", INDEX.read_bytes())
        elif path == "/api/health":
            self.send_json(200, service_health(self.server.ollama_url))
        elif path == "/favicon.ico":
            self.send_bytes(204, "image/x-icon", b"")
        else:
            self.send_json(404, {"error": "찾을 수 없습니다."})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] != "/api/analyze":
            self.send_json(404, {"error": "찾을 수 없습니다."})
            return
        try:
            content_type = self.headers.get("Content-Type", "")
            if not content_type.startswith("application/json"):
                raise APIError(415, "application/json 요청만 허용합니다.")
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                raise APIError(400, "요청 본문이 비어 있습니다.")
            if length > MAX_REQUEST_BYTES:
                raise APIError(413, "요청 크기는 최대 40MB입니다.")
            payload = json.loads(self.rfile.read(length))
            files = decode_upload(payload.get("files") if isinstance(payload, dict) else None)
            self.send_json(200, analyze_project(files, self.server.ollama_url))
        except APIError as exc:
            self.send_json(exc.status, {"error": str(exc)})
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "요청 JSON 형식이 올바르지 않습니다."})
        except Exception as exc:  # keep parser/tool failures out of the browser
            print(f"analysis_error={type(exc).__name__}: {exc}")
            self.send_json(500, {"error": "분석 중 예상하지 못한 오류가 발생했습니다."})

    def log_message(self, format: str, *args: object) -> None:
        print(f"http={self.address_string()} {format % args}")


class Server(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], ollama_url: str):
        super().__init__(address, Handler)
        self.ollama_url = ollama_url


def self_check() -> None:
    def encoded(path: str, content: bytes) -> dict:
        return {"path": f"demo/{path}", "content_base64": base64.b64encode(content).decode()}

    manifest = {
        "subjects": [
            {"path": "media/hero.png", "description": "blue hero", "origin_type": "third_party_free"},
            {"path": "deliverables/site.zip", "description": "site", "origin_type": "output"},
        ]
    }
    records = [
        encoded(OBSERVATIONS, json.dumps(manifest).encode()),
        encoded("media/hero.png", b"image"),
        encoded("deliverables/site.zip", b"output"),
        encoded("evidence/source/source.txt", b"Source: media/hero.png"),
        encoded("evidence/license/license.txt", b"License: media/hero.png"),
        encoded("lineage/site.md", b"Output: deliverables/site.zip\nIngredient: media/hero.png\n"),
    ]
    files = decode_upload(records)
    result = analyze_project(files, DEFAULT_OLLAMA_URL, run_c2pa=False)
    assert len(result["relations"]) == 3
    assert result["missing_evidence"] == []
    assert result["ai"]["semantic_tasks"] == 0
    assert result["legal_conclusions"] == []
    try:
        decode_upload([encoded("../escape.txt", b"bad")])
    except APIError:
        pass
    else:
        raise AssertionError("path traversal was not rejected")
    print("PASS: exact relation flow, missing-evidence calculation, and path guard")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local RightsLedger MVP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    server = Server((args.host, args.port), args.ollama_url)
    print(f"RightsLedger {APP_VERSION}: http://{args.host}:{args.port}")
    print("No uploads are persisted; Ctrl-C stops the local server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
