#!/usr/bin/env python3
"""Minimal, reproducible falsification harness for RightsLedger."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CASES = ROOT / "cases"
TRUTH = ROOT / "ground_truth"
RESULTS = ROOT / "results"
OBSERVATIONS = ".rightsledger_observations.json"
MODEL = "bge-m3:latest"
BASELINE_MODEL = "qwen3:4b"
BASELINE_PROMPT = ROOT / "general_llm_baseline_prompt_v1.md"
BASELINE_SEED = 20260904
BASELINE_CONTEXT = 32768
MIN_SIMILARITY = 0.58
MIN_MARGIN = 0.025
REQUIREMENTS = {
    "third_party_free": {"source", "license"},
    "purchased": {"receipt", "license"},
    "open_source": {"source", "license"},
    "ai_generated": {"prompt", "model_terms"},
    "original": {"author"},
    "output": set(),
}


def subject(path: str, description: str, origin_type: str) -> dict:
    return {"path": path, "description": description, "origin_type": origin_type}


def evidence(kind: str, name: str, text: str, *subjects: str) -> dict:
    return {
        "path": f"evidence/{kind}/{name}",
        "kind": kind,
        "text": text,
        "subjects": list(subjects),
    }


def lineage(path: str, output: str, pairs: list[tuple[str, str]]) -> dict:
    return {"path": path, "output": output, "pairs": pairs}


def specs() -> list[dict]:
    return [
        {
            "case_id": "CASE-001",
            "title": "explicit path control",
            "subjects": [
                subject("media/hero_skyline.png", "wide blue night city skyline used as a hero background", "third_party_free"),
                subject("audio/calm_piano.wav", "calm piano instrumental bed for the launch video", "purchased"),
                subject("src/player.js", "JavaScript audio player adapted from the WaveKit project", "open_source"),
                subject("generated/tagline.png", "AI-generated Korean campaign tagline on a transparent background", "ai_generated"),
                subject("deliverables/launch_video.mp4", "launch video combining the skyline, piano bed and tagline", "output"),
            ],
            "evidence": [
                evidence("source", "hero_source.txt", "Source for media/hero_skyline.png: https://example.test/skyline", "media/hero_skyline.png"),
                evidence("license", "hero_license.txt", "License for media/hero_skyline.png: CC BY 4.0", "media/hero_skyline.png"),
                evidence("receipt", "piano_receipt.txt", "Purchase receipt for audio/calm_piano.wav, order SYN-1001", "audio/calm_piano.wav"),
                evidence("license", "piano_license.txt", "Commercial media license for audio/calm_piano.wav", "audio/calm_piano.wav"),
                evidence("source", "player_source.txt", "Upstream source for src/player.js: https://example.test/wavekit", "src/player.js"),
                evidence("license", "player_license.txt", "SPDX-License-Identifier: MIT\nApplies to src/player.js", "src/player.js"),
                evidence("prompt", "tagline_prompt.txt", "Prompt record for generated/tagline.png: warm Korean launch phrase", "generated/tagline.png"),
                evidence("model_terms", "tagline_terms.txt", "Model terms snapshot for generated/tagline.png, tool: SyntheticCanvas", "generated/tagline.png"),
            ],
            "lineage": [
                lineage(
                    "lineage/launch_video.md",
                    "deliverables/launch_video.mp4",
                    [
                        ("media/hero_skyline.png", "media/hero_skyline.png"),
                        ("audio/calm_piano.wav", "audio/calm_piano.wav"),
                        ("generated/tagline.png", "generated/tagline.png"),
                    ],
                )
            ],
            "fillers": {"README.md": "Synthetic control project with explicit file references."},
        },
        {
            "case_id": "CASE-002",
            "title": "renamed multilingual campaign assets",
            "subjects": [
                subject("media/img_1042.png", "neon-lit evening food market photographed at street level", "third_party_free"),
                subject("audio/track_final.wav", "energetic hand-drum rhythm purchased for a short social reel", "purchased"),
                subject("src/lib_a.js", "bar chart component adapted from the OpenPlot Mini library", "open_source"),
                subject("generated/voice_take.wav", "synthetic Korean narrator saying the weekend market invitation", "ai_generated"),
                subject("deliverables/reel_v7.mp4", "vertical weekend-market reel with night street, drums, chart and Korean narration", "output"),
            ],
            "evidence": [
                evidence("source", "night_market_origin.txt", "원본 주소: 네온 간판이 빛나는 야시장 골목의 거리 사진", "media/img_1042.png"),
                evidence("license", "street_photo_permission.txt", "Attribution license for the night street food market photograph", "media/img_1042.png"),
                evidence("receipt", "rhythm_order.txt", "Receipt for the energetic hand-drum loop used in the weekend reel", "audio/track_final.wav"),
                evidence("license", "percussion_terms.txt", "Commercial synchronization license for the upbeat percussion recording", "audio/track_final.wav"),
                evidence("source", "chart_upstream.txt", "Upstream repository for the OpenPlot Mini bar-chart component", "src/lib_a.js"),
                evidence("license", "chart_mit.txt", "MIT license notice for the adapted OpenPlot Mini chart component", "src/lib_a.js"),
                evidence("prompt", "narration_prompt.txt", "생성 프롬프트: 주말 야시장으로 초대하는 밝은 한국어 여성 내레이션", "generated/voice_take.wav"),
            ],
            "lineage": [
                lineage(
                    "lineage/reel_notes.md",
                    "deliverables/reel_v7.mp4",
                    [
                        ("media/img_1042.png", "a neon-lit evening food market scene photographed at street level"),
                        ("audio/track_final.wav", "an energetic purchased hand-drum rhythm"),
                        ("src/lib_a.js", "the adapted OpenPlot Mini bar chart component"),
                        ("generated/voice_take.wav", "a synthetic Korean weekend-market invitation voice"),
                    ],
                )
            ],
            "fillers": {
                "README.md": "Files were renamed during export. Descriptions remain in project notes.",
                "notes/edit_log.md": "The editor normalized media filenames before final render.",
            },
        },
        {
            "case_id": "CASE-003",
            "title": "similar audio alternatives and missing purchase evidence",
            "subjects": [
                subject("media/a_17.wav", "standard-tempo gentle acoustic guitar recording selected for the podcast intro", "purchased"),
                subject("media/a_18.wav", "slower alternate gentle acoustic guitar recording not selected for the intro", "purchased"),
                subject("media/photo_x.png", "founder portrait photographed beside a window in soft daylight", "original"),
                subject("generated/music_sting.wav", "short electronic three-note logo sting generated for the show", "ai_generated"),
                subject("deliverables/podcast_ep1.wav", "first podcast episode with acoustic intro and electronic logo sting", "output"),
            ],
            "evidence": [
                evidence("receipt", "guitar_standard_order.txt", "Order receipt for the standard-tempo acoustic guitar intro recording", "media/a_17.wav"),
                evidence("license", "guitar_standard_license.txt", "Podcast synchronization license for the selected standard-tempo gentle guitar take", "media/a_17.wav"),
                evidence("author", "portrait_author.txt", "Team authorship statement for the founder portrait shot in window light", "media/photo_x.png"),
                evidence("prompt", "sting_prompt.txt", "Prompt: a concise electronic three-note sonic logo for a podcast", "generated/music_sting.wav"),
                evidence("model_terms", "sting_model_terms.txt", "Terms snapshot for the audio model used to create the electronic three-note logo sting", "generated/music_sting.wav"),
            ],
            "lineage": [
                lineage(
                    "lineage/episode_cue.md",
                    "deliverables/podcast_ep1.wav",
                    [
                        ("media/a_17.wav", "the selected standard-tempo gentle acoustic guitar intro"),
                        ("generated/music_sting.wav", "the generated electronic three-note show logo"),
                    ],
                )
            ],
            "fillers": {
                "README.md": "Two similar guitar takes remain in the folder.",
                "notes/guest_topics.md": "Synthetic interview topic list.",
                "notes/mix_settings.txt": "Intro -12 LUFS; speech -16 LUFS.",
                "exports/cover_preview.txt": "Placeholder for a non-audited preview export.",
            },
        },
        {
            "case_id": "CASE-004",
            "title": "renamed open-source dashboard components",
            "subjects": [
                subject("src/c_01.js", "date formatting helper adapted from the ChronosLite package", "open_source"),
                subject("src/c_02.js", "custom event filter written entirely by the project team", "original"),
                subject("media/i_77.svg", "outline calendar icon from the OpenGlyph collection", "third_party_free"),
                subject("media/i_78.svg", "outline clock icon from the OpenGlyph collection", "third_party_free"),
                subject("deliverables/dashboard.zip", "dashboard bundle containing date helper, custom filter and two outline icons", "output"),
            ],
            "evidence": [
                evidence("source", "chronos_upstream.txt", "Repository URL for the ChronosLite date-formatting helper", "src/c_01.js"),
                evidence("license", "chronos_license.txt", "MIT license notice for the ChronosLite date utility", "src/c_01.js"),
                evidence("author", "filter_authorship.txt", "Team declaration for the custom event filtering module", "src/c_02.js"),
                evidence("source", "calendar_icon_source.txt", "Source page for the outline calendar symbol in OpenGlyph", "media/i_77.svg"),
                evidence("license", "calendar_icon_license.txt", "CC BY license for the OpenGlyph outline calendar symbol", "media/i_77.svg"),
                evidence("source", "clock_icon_source.txt", "Source page for the outline clock symbol in OpenGlyph", "media/i_78.svg"),
                evidence("license", "clock_icon_license.txt", "CC BY license for the OpenGlyph outline clock symbol", "media/i_78.svg"),
            ],
            "lineage": [
                lineage(
                    "lineage/dashboard_bundle.md",
                    "deliverables/dashboard.zip",
                    [
                        ("src/c_01.js", "the ChronosLite date-formatting helper"),
                        ("src/c_02.js", "the team's custom event filter"),
                        ("media/i_77.svg", "the outline calendar symbol from OpenGlyph"),
                        ("media/i_78.svg", "the outline clock symbol from OpenGlyph"),
                    ],
                )
            ],
            "fillers": {
                "README.md": "Synthetic dashboard build.",
                "package.json": "{\"name\":\"synthetic-dashboard\",\"private\":true}",
            },
        },
        {
            "case_id": "CASE-005",
            "title": "AI landing page with an unrelated source record",
            "subjects": [
                subject("generated/g_amber.png", "AI-generated amber glass bottle product render on white", "ai_generated"),
                subject("generated/g_ocean.png", "AI-generated blue ocean texture used as a background", "ai_generated"),
                subject("media/font_z.woff", "rounded display typeface used for the product headline", "third_party_free"),
                subject("src/landing.css", "landing-page layout styles written by the project team", "original"),
                subject("deliverables/landing_page.zip", "landing page with amber bottle, ocean background, rounded headline and custom CSS", "output"),
            ],
            "evidence": [
                evidence("prompt", "amber_prompt.txt", "Prompt record: photoreal amber glass bottle centered on a clean white studio background", "generated/g_amber.png"),
                evidence("model_terms", "amber_terms.txt", "Terms snapshot for the image model used for the amber bottle render", "generated/g_amber.png"),
                evidence("prompt", "ocean_prompt.txt", "Prompt record: abstract blue ocean-water texture seen from above", "generated/g_ocean.png"),
                evidence("model_terms", "ocean_terms.txt", "Terms snapshot for the image model used for the blue ocean texture", "generated/g_ocean.png"),
                evidence("license", "rounded_type_license.txt", "Open font license for the rounded display typeface used in the headline", "media/font_z.woff"),
                evidence("source", "unrelated_drone_source.txt", "Source URL for mountain drone footage used in an abandoned travel-film draft"),
                evidence("author", "css_authorship.txt", "Team authorship statement for the custom landing-page layout stylesheet", "src/landing.css"),
            ],
            "lineage": [
                lineage(
                    "lineage/landing_bundle.md",
                    "deliverables/landing_page.zip",
                    [
                        ("generated/g_amber.png", "the AI-created amber glass bottle product render"),
                        ("generated/g_ocean.png", "the AI-created blue ocean background texture"),
                        ("media/font_z.woff", "the rounded display headline typeface"),
                        ("src/landing.css", "the team's custom landing-page layout styles"),
                    ],
                )
            ],
            "fillers": {
                "README.md": "Synthetic product landing page.",
                "notes/provenance_notes.md": "One source record belongs to an abandoned draft and must not be auto-attached.",
            },
        },
    ]


def dump_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate() -> None:
    for spec in specs():
        case_dir = CASES / spec["case_id"] / "project"
        truth_relations = []
        files = []

        for item in spec["subjects"]:
            path = case_dir / item["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(("SYNTHETIC PLACEHOLDER\n" + item["description"] + "\n").encode())
            files.append(item["path"])

        for item in spec["evidence"]:
            path = case_dir / item["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(item["text"] + "\n", encoding="utf-8")
            files.append(item["path"])
            for asset in item["subjects"]:
                truth_relations.append(
                    {"relation_type": f"evidence:{item['kind']}", "from": asset, "to": item["path"]}
                )

        for item in spec["lineage"]:
            lines = [f"Output: {item['output']}"]
            for asset, clue in item["pairs"]:
                lines.append(f"Ingredient: {clue}")
                truth_relations.append({"relation_type": "ingredient", "from": item["output"], "to": asset})
            path = case_dir / item["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            files.append(item["path"])

        for relpath, content in spec["fillers"].items():
            path = case_dir / relpath
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content + "\n", encoding="utf-8")
            files.append(relpath)

        assert len(files) == 15, (spec["case_id"], len(files))
        dump_json(case_dir / OBSERVATIONS, {"subjects": spec["subjects"]})

        provided = {}
        for rel in truth_relations:
            if rel["relation_type"].startswith("evidence:"):
                provided.setdefault(rel["from"], set()).add(rel["relation_type"].split(":", 1)[1])
        missing = []
        for item in spec["subjects"]:
            for kind in sorted(REQUIREMENTS[item["origin_type"]] - provided.get(item["path"], set())):
                missing.append({"asset": item["path"], "evidence_type": kind})

        dump_json(
            TRUTH / f"{spec['case_id']}.json",
            {
                "case_id": spec["case_id"],
                "title": spec["title"],
                "assets": sorted(files),
                "relations": sorted(truth_relations, key=relation_key),
                "missing_evidence": missing,
            },
        )
    print(f"generated_cases={len(specs())} assets_per_case=15")


def relation_key(item: dict) -> tuple:
    return item["relation_type"], item["from"], item["to"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def exact_matches(text: str, subjects: list[dict]) -> list[str]:
    lowered = text.lower()
    matches = []
    for item in subjects:
        path = item["path"].lower()
        name = Path(path).name
        if path in lowered or name in lowered:
            matches.append(item["path"])
    return matches


def cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norms = math.sqrt(sum(a * a for a in left) * sum(b * b for b in right))
    return dot / norms if norms else 0.0


class OllamaEmbedder:
    def __init__(self, base_url: str):
        self.url = base_url.rstrip("/") + "/api/embed"
        self.cache: dict[str, list[float]] = {}

    def prepare(self, texts: list[str]) -> None:
        missing = list(dict.fromkeys(text for text in texts if text not in self.cache))
        if not missing:
            return
        body = json.dumps({"model": MODEL, "input": missing}).encode()
        request = urllib.request.Request(self.url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.load(response)
        vectors = payload.get("embeddings", [])
        if len(vectors) != len(missing):
            raise RuntimeError(f"Expected {len(missing)} embeddings, received {len(vectors)}")
        self.cache.update(zip(missing, vectors))

    def get(self, text: str) -> list[float]:
        return self.cache[text]


def asset_doc(item: dict) -> str:
    return f"Asset description: {item['description']}. Declared origin: {item['origin_type']}."


def semantic_match(clue: str, candidates: list[dict], embedder: OllamaEmbedder) -> tuple[str | None, list[dict]]:
    ranked = sorted(
        ({"asset": item["path"], "score": cosine(embedder.get(clue), embedder.get(asset_doc(item)))} for item in candidates),
        key=lambda item: item["score"],
        reverse=True,
    )
    if not ranked:
        return None, []
    margin = ranked[0]["score"] - (ranked[1]["score"] if len(ranked) > 1 else 0.0)
    accepted = ranked[0]["score"] >= MIN_SIMILARITY and margin >= MIN_MARGIN
    return (ranked[0]["asset"] if accepted else None), ranked[:3]


def baseline_prompt_text() -> str:
    text = BASELINE_PROMPT.read_text(encoding="utf-8")
    match = re.search(r"<!-- PROMPT_START -->\s*(.*?)\s*<!-- PROMPT_END -->", text, re.DOTALL)
    if not match:
        raise RuntimeError("Baseline prompt markers are missing")
    return match.group(1).strip()


def project_dossier(case_id: str) -> tuple[str, list[str]]:
    project = CASES / case_id / "project"
    paths = sorted(
        path for path in project.rglob("*") if path.is_file() and path.name != OBSERVATIONS
    )
    sections = []
    for path in paths:
        data = path.read_bytes()
        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError:
            content = f"[binary file: {len(data)} bytes, sha256={sha256(path)}]"
        sections.append(
            f"### FILE: {path.relative_to(project).as_posix()}\n```text\n{content.rstrip()}\n```"
        )
    return "\n\n".join(sections), [path.relative_to(project).as_posix() for path in paths]


def final_content(raw_content: str) -> tuple[str, bool]:
    if "</think>" not in raw_content:
        return raw_content.strip(), False
    return raw_content.rsplit("</think>", 1)[1].strip(), True


def run_llm_baseline(ollama_url: str) -> None:
    prompt = baseline_prompt_text()
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    output_dir = RESULTS / "general_llm_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for spec in specs():
        case_id = spec["case_id"]
        dossier, input_paths = project_dossier(case_id)
        user_content = f"{prompt}\n\n## 프로젝트 입력\n\n{dossier}"
        body = json.dumps(
            {
                "model": BASELINE_MODEL,
                "messages": [{"role": "user", "content": user_content}],
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0,
                    "seed": BASELINE_SEED,
                    "num_ctx": BASELINE_CONTEXT,
                },
            }
        ).encode()
        request = urllib.request.Request(
            ollama_url.rstrip("/") + "/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=300) as response:
            raw_response = json.load(response)
        raw_content = raw_response.get("message", {}).get("content", "")
        checklist, stripped_thinking = final_content(raw_content)
        if not checklist:
            raise RuntimeError(f"Empty baseline checklist for {case_id}")
        (output_dir / f"{case_id}.md").write_text(checklist + "\n", encoding="utf-8")
        records.append(
            {
                "case_id": case_id,
                "model": BASELINE_MODEL,
                "model_local_id": "359d7dd4bcda",
                "options": {
                    "temperature": 0,
                    "seed": BASELINE_SEED,
                    "num_ctx": BASELINE_CONTEXT,
                    "think": False,
                },
                "prompt_sha256": prompt_hash,
                "input_paths": input_paths,
                "input_sha256": hashlib.sha256(user_content.encode()).hexdigest(),
                "output_sha256": hashlib.sha256(checklist.encode()).hexdigest(),
                "stripped_inline_thinking": stripped_thinking,
                "raw_response": raw_response,
            }
        )
        print(f"case={case_id} checklist_chars={len(checklist)}")
    raw_path = RESULTS / "general_llm_raw.jsonl"
    raw_path.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records),
        encoding="utf-8",
    )
    metrics = {
        "mode": "general_llm_checklist",
        "model": BASELINE_MODEL,
        "model_local_id": "359d7dd4bcda",
        "case_count": len(records),
        "temperature": 0,
        "seed": BASELINE_SEED,
        "num_ctx": BASELINE_CONTEXT,
        "thinking_requested": False,
        "responses_requiring_inline_thinking_strip": sum(
            item["stripped_inline_thinking"] for item in records
        ),
        "inference_duration_seconds": sum(
            item["raw_response"].get("total_duration", 0) for item in records
        )
        / 1_000_000_000,
        "human_review_time_seconds": None,
        "accuracy_metrics": None,
    }
    dump_json(RESULTS / "general_llm_run_metrics.json", metrics)
    print(f"mode=general_llm cases={len(records)} human_review=pending accuracy=pending")


def predict_case(case_id: str, mode: str, embedder: OllamaEmbedder | None) -> dict:
    project = CASES / case_id / "project"
    observations = json.loads((project / OBSERVATIONS).read_text(encoding="utf-8"))["subjects"]
    inputs = [item for item in observations if item["origin_type"] != "output"]
    outputs = [item for item in observations if item["origin_type"] == "output"]
    evidence_files = sorted((project / "evidence").glob("*/*"))
    lineage_files = sorted((project / "lineage").glob("*.md"))

    clue_texts = [path.read_text(encoding="utf-8").strip() for path in evidence_files]
    for path in lineage_files:
        clue_texts.extend(
            line.split(":", 1)[1].strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("Ingredient:")
        )
    if mode == "hybrid":
        assert embedder is not None
        embedder.prepare(clue_texts + [asset_doc(item) for item in inputs])

    relations: list[dict] = []
    unresolved: list[dict] = []

    for path in evidence_files:
        relpath = path.relative_to(project).as_posix()
        kind = path.parent.name
        text = path.read_text(encoding="utf-8").strip()
        candidates = [item for item in inputs if kind in REQUIREMENTS[item["origin_type"]]]
        exact = exact_matches(text, candidates)
        if exact:
            for asset in exact:
                relations.append({"relation_type": f"evidence:{kind}", "from": asset, "to": relpath, "method": "exact"})
            continue
        if mode == "hybrid":
            match, scores = semantic_match(text, candidates, embedder)
            if match:
                relations.append({"relation_type": f"evidence:{kind}", "from": match, "to": relpath, "method": "embedding"})
                continue
            unresolved.append({"clue": relpath, "kind": f"evidence:{kind}", "scores": scores})
        else:
            unresolved.append({"clue": relpath, "kind": f"evidence:{kind}", "scores": []})

    for path in lineage_files:
        relpath = path.relative_to(project).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        output_text = next(line.split(":", 1)[1].strip() for line in lines if line.startswith("Output:"))
        output_match = exact_matches(output_text, outputs)
        if len(output_match) != 1:
            unresolved.append({"clue": relpath, "kind": "lineage_output", "scores": []})
            continue
        for index, line in enumerate(
            (line for line in lines if line.startswith("Ingredient:")), start=1
        ):
            clue = line.split(":", 1)[1].strip()
            exact = exact_matches(clue, inputs)
            if exact:
                for asset in exact:
                    relations.append({"relation_type": "ingredient", "from": output_match[0], "to": asset, "method": "exact"})
                continue
            if mode == "hybrid":
                match, scores = semantic_match(clue, inputs, embedder)
                if match:
                    relations.append({"relation_type": "ingredient", "from": output_match[0], "to": match, "method": "embedding"})
                    continue
                unresolved.append({"clue": f"{relpath}#ingredient-{index}", "kind": "ingredient", "scores": scores})
            else:
                unresolved.append({"clue": f"{relpath}#ingredient-{index}", "kind": "ingredient", "scores": []})

    unique = {relation_key(item): item for item in relations}
    relations = sorted(unique.values(), key=relation_key)
    provided = {}
    for rel in relations:
        if rel["relation_type"].startswith("evidence:"):
            provided.setdefault(rel["from"], set()).add(rel["relation_type"].split(":", 1)[1])
    missing = []
    for item in inputs:
        for kind in sorted(REQUIREMENTS[item["origin_type"]] - provided.get(item["path"], set())):
            missing.append({"asset": item["path"], "evidence_type": kind})

    inventory = []
    for path in sorted(item for item in project.rglob("*") if item.is_file() and item.name != OBSERVATIONS):
        inventory.append({"path": path.relative_to(project).as_posix(), "sha256": sha256(path)})
    return {
        "case_id": case_id,
        "mode": mode,
        "model": MODEL if mode == "hybrid" else None,
        "thresholds": {"min_similarity": MIN_SIMILARITY, "min_margin": MIN_MARGIN} if mode == "hybrid" else None,
        "inventory": inventory,
        "relations": relations,
        "missing_evidence": missing,
        "unresolved": unresolved,
        "legal_conclusions": [],
    }


def prf(predicted: set, expected: set) -> dict:
    tp = len(predicted & expected)
    precision = tp / len(predicted) if predicted else (1.0 if not expected else 0.0)
    recall = tp / len(expected) if expected else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "predicted": len(predicted), "expected": len(expected), "precision": precision, "recall": recall, "f1": f1}


def evaluate(predictions: list[dict]) -> dict:
    all_pred_assets, all_true_assets = set(), set()
    all_pred_relations, all_true_relations = set(), set()
    all_pred_missing, all_true_missing = set(), set()
    legal_count = unresolved_count = 0
    per_case = []

    for prediction in predictions:
        case_id = prediction["case_id"]
        truth = json.loads((TRUTH / f"{case_id}.json").read_text(encoding="utf-8"))
        pred_assets = {(case_id, item["path"]) for item in prediction["inventory"]}
        true_assets = {(case_id, item) for item in truth["assets"]}
        pred_rel = {(case_id, *relation_key(item)) for item in prediction["relations"]}
        true_rel = {(case_id, *relation_key(item)) for item in truth["relations"]}
        pred_missing = {(case_id, item["asset"], item["evidence_type"]) for item in prediction["missing_evidence"]}
        true_missing = {(case_id, item["asset"], item["evidence_type"]) for item in truth["missing_evidence"]}

        all_pred_assets |= pred_assets
        all_true_assets |= true_assets
        all_pred_relations |= pred_rel
        all_true_relations |= true_rel
        all_pred_missing |= pred_missing
        all_true_missing |= true_missing
        legal_count += len(prediction["legal_conclusions"])
        unresolved_count += len(prediction["unresolved"])
        per_case.append(
            {
                "case_id": case_id,
                "asset_discovery": prf(pred_assets, true_assets),
                "relations": prf(pred_rel, true_rel),
                "missing_evidence": prf(pred_missing, true_missing),
                "unresolved_clues": len(prediction["unresolved"]),
            }
        )

    return {
        "mode": predictions[0]["mode"],
        "model": predictions[0]["model"],
        "case_count": len(predictions),
        "asset_discovery": prf(all_pred_assets, all_true_assets),
        "relations": prf(all_pred_relations, all_true_relations),
        "missing_evidence": prf(all_pred_missing, all_true_missing),
        "legal_conclusion_count": legal_count,
        "unresolved_clues": unresolved_count,
        "review_proxy_units": unresolved_count + len(all_pred_missing),
        "per_case": per_case,
    }


def run(mode: str, ollama_url: str) -> None:
    if not TRUTH.exists():
        generate()
    embedder = OllamaEmbedder(ollama_url) if mode == "hybrid" else None
    predictions = [predict_case(spec["case_id"], mode, embedder) for spec in specs()]
    RESULTS.mkdir(parents=True, exist_ok=True)
    prediction_path = RESULTS / f"{mode}_predictions.jsonl"
    prediction_path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in predictions), encoding="utf-8")
    metrics = evaluate(predictions)
    dump_json(RESULTS / f"{mode}_metrics.json", metrics)
    print(
        f"mode={mode} assets_recall={metrics['asset_discovery']['recall']:.3f} "
        f"relation_f1={metrics['relations']['f1']:.3f} "
        f"missing_recall={metrics['missing_evidence']['recall']:.3f} "
        f"review_proxy={metrics['review_proxy_units']}"
    )


def error_analysis(mode: str) -> dict:
    predictions = [
        json.loads(line)
        for line in (RESULTS / f"{mode}_predictions.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    errors = {
        "relation_false_negatives": [],
        "relation_false_positives": [],
        "missing_evidence_false_negatives": [],
        "missing_evidence_false_positives": [],
        "unresolved_clues": [],
    }
    for prediction in predictions:
        case_id = prediction["case_id"]
        truth = json.loads((TRUTH / f"{case_id}.json").read_text(encoding="utf-8"))
        predicted_relations = {relation_key(item) for item in prediction["relations"]}
        expected_relations = {relation_key(item) for item in truth["relations"]}
        predicted_missing = {
            (item["asset"], item["evidence_type"]) for item in prediction["missing_evidence"]
        }
        expected_missing = {
            (item["asset"], item["evidence_type"]) for item in truth["missing_evidence"]
        }
        for relation_type, source, target in sorted(expected_relations - predicted_relations):
            errors["relation_false_negatives"].append(
                {"case_id": case_id, "relation_type": relation_type, "from": source, "to": target}
            )
        for relation_type, source, target in sorted(predicted_relations - expected_relations):
            errors["relation_false_positives"].append(
                {"case_id": case_id, "relation_type": relation_type, "from": source, "to": target}
            )
        for asset, evidence_type in sorted(expected_missing - predicted_missing):
            errors["missing_evidence_false_negatives"].append(
                {"case_id": case_id, "asset": asset, "evidence_type": evidence_type}
            )
        for asset, evidence_type in sorted(predicted_missing - expected_missing):
            errors["missing_evidence_false_positives"].append(
                {"case_id": case_id, "asset": asset, "evidence_type": evidence_type}
            )
        for item in prediction["unresolved"]:
            errors["unresolved_clues"].append({"case_id": case_id, **item})
    return errors


def compare() -> None:
    deterministic = json.loads((RESULTS / "deterministic_metrics.json").read_text(encoding="utf-8"))
    hybrid = json.loads((RESULTS / "hybrid_metrics.json").read_text(encoding="utf-8"))
    baseline_metrics_path = RESULTS / "general_llm_run_metrics.json"
    baseline_metrics = (
        json.loads(baseline_metrics_path.read_text(encoding="utf-8"))
        if baseline_metrics_path.exists()
        else None
    )
    hybrid_errors = error_analysis("hybrid")
    base_units = deterministic["review_proxy_units"]
    reduction = 1 - hybrid["review_proxy_units"] / base_units if base_units else 0.0
    gates = {
        "asset_discovery_recall_gte_0_95": hybrid["asset_discovery"]["recall"] >= 0.95,
        "relation_f1_gte_0_85": hybrid["relations"]["f1"] >= 0.85,
        "missing_evidence_recall_eq_1": hybrid["missing_evidence"]["recall"] == 1.0,
        "legal_conclusion_count_eq_0": hybrid["legal_conclusion_count"] == 0,
        "review_proxy_reduction_gte_0_50": reduction >= 0.50,
        "human_time_reduction_gte_0_50": None,
    }
    technical_pass = all(value for key, value in gates.items() if key != "human_time_reduction_gte_0_50")
    comparison = {
        "experiment_date": "2026-09-04",
        "scope": "relation_linker_component_spike",
        "model": MODEL,
        "deterministic": deterministic,
        "hybrid": hybrid,
        "relation_f1_delta": hybrid["relations"]["f1"] - deterministic["relations"]["f1"],
        "review_proxy_reduction": reduction,
        "gates": gates,
        "hybrid_error_analysis": hybrid_errors,
        "general_llm_baseline_run": baseline_metrics,
        "preregistered_protocol_completion": {
            "five_synthetic_projects": True,
            "fifteen_auditable_files_per_project": True,
            "fifteen_primary_assets_per_project": False,
            "general_llm_checklist_outputs": baseline_metrics is not None,
            "general_llm_checklist_blind_scoring": False,
            "c2pa_case": False,
            "real_media_understanding": False,
            "human_time_test": False,
        },
        "technical_verdict": "pass" if technical_pass else "fail",
        "overall_verdict": "component_pass_full_24h_gate_incomplete" if technical_pass else "component_fail",
        "candidate_status": "retain_for_blind_validation_not_selected" if technical_pass else "reconsider_candidate",
    }
    dump_json(RESULTS / "comparison_2026-09-04.json", comparison)
    relation_fn = hybrid_errors["relation_false_negatives"]
    missing_fp = hybrid_errors["missing_evidence_false_positives"]
    unresolved = hybrid_errors["unresolved_clues"]
    relation_fn_text = "\n".join(
        f"- `{item['case_id']}`: `{item['relation_type']}` `{item['from']}` → `{item['to']}`"
        for item in relation_fn
    ) or "- 없음"
    missing_fp_text = "\n".join(
        f"- `{item['case_id']}`: `{item['asset']}`의 `{item['evidence_type']}`를 누락으로 과잉 경고"
        for item in missing_fp
    ) or "- 없음"
    unresolved_text = "\n".join(
        f"- `{item['case_id']}` `{item['clue']}`: 최고 유사도 "
        f"{item['scores'][0]['score']:.3f} (`{item['scores'][0]['asset']}`)"
        if item["scores"]
        else f"- `{item['case_id']}` `{item['clue']}`: 후보 없음"
        for item in unresolved
    ) or "- 없음"
    report = f"""# RightsLedger 관계 연결 기술 스파이크 결과

- 실행일: 2026-09-04, Asia/Seoul
- 범위: 사전 등록한 24시간 반증 실험 중 `관계 후보 연결` 구성요소
- 모델: 로컬 `{MODEL}` 임베딩
- 외부 데이터 전송: 없음
- 원시 결과: `comparison_2026-09-04.json`

## OBSERVATION — 직접 측정

| 지표 | 결정론 기준선 | 임베딩 하이브리드 | 사전 기준 |
|---|---:|---:|---:|
| 자산 발견 재현율 | {deterministic['asset_discovery']['recall']:.3f} | {hybrid['asset_discovery']['recall']:.3f} | 0.95 이상 |
| 관계 정밀도 | {deterministic['relations']['precision']:.3f} | {hybrid['relations']['precision']:.3f} | 보조지표 |
| 관계 재현율 | {deterministic['relations']['recall']:.3f} | {hybrid['relations']['recall']:.3f} | 보조지표 |
| 관계 F1 | {deterministic['relations']['f1']:.3f} | {hybrid['relations']['f1']:.3f} | 0.85 이상 |
| 누락 증거 정밀도 | {deterministic['missing_evidence']['precision']:.3f} | {hybrid['missing_evidence']['precision']:.3f} | 보조지표 |
| 누락 증거 재현율 | {deterministic['missing_evidence']['recall']:.3f} | {hybrid['missing_evidence']['recall']:.3f} | 1.00 |
| 법률 결론 생성 | {deterministic['legal_conclusion_count']} | {hybrid['legal_conclusion_count']} | 0건 |
| 검토 작업량 대리지표 | {deterministic['review_proxy_units']} | {hybrid['review_proxy_units']} | 50% 감소 |

- 관계 F1 변화: {comparison['relation_f1_delta']:+.3f}
- 검토 작업량 대리지표 감소: {reduction:.1%}
- 구성요소 기술 게이트: **{comparison['technical_verdict']}**
- 전체 판정: **{comparison['overall_verdict']}**
- 후보 상태: **{comparison['candidate_status']}**

## OBSERVATION — 오차 분석

### 관계 거짓 음성

{relation_fn_text}

### 누락 증거 거짓 양성

{missing_fp_text}

### 자동 연결을 보류한 단서

{unresolved_text}

`CASE-002`의 `percussion_terms.txt`는 실제 음악 라이선스였지만 최고 유사도 0.521로 사전 임계값 0.58에 못 미쳤다. 이 한 번의 보류가 관계 거짓 음성 1건과 누락 증거 거짓 양성 1건을 함께 만들었다. 결과를 본 뒤 임계값을 낮추지 않았다. `CASE-005`의 무관한 드론 출처 기록은 올바르게 보류됐다.

## 프로토콜 충족 여부

| 항목 | 사전 계획 | 이번 실행 | 판정 |
|---|---|---|---|
| 합성 프로젝트 | 5개 | 5개 | 충족 |
| 프로젝트당 입력 규모 | 주 자산 15개 | 감사 대상 파일 15개, 주 자산 5개 | 부분 충족 |
| 비교 기준선 | 범용 생성형 LLM 자유형 체크리스트 | `qwen3:4b` 출력 5건 확보, 블라인드 채점 전 | 부분 실행 |
| 의미 연결 | AI 관계 후보 생성 | 로컬 `bge-m3` | 실행 |
| C2PA 사례 | 포함 | `c2patool` 부재, 제외 | 미실행 |
| 실제 미디어 이해 | 포함 가능 | 사전 작성 설명 사용 | 미실행 |
| 사람 감사 시간 | 50% 감소 | 작업량 대리지표만 계산 | 미실행 |

따라서 이 결과는 원래의 24시간 반증 실험 전체 통과가 아니다. `관계 후보 생성에 AI를 쓸 기술적 이유가 있는가`라는 더 좁은 질문만 통과했다.

## INTERPRETATION

하이브리드가 관계 F1과 누락 탐지 기준을 넘었다면, 정확 파일명 검색만으로는 복원하지 못한 자연어 단서를 의미 임베딩이 연결했다는 뜻이다. 이는 RightsLedger의 AI 역할을 `법률 판단`이 아니라 `이질적인 기록 사이의 관계 후보 생성`으로 제한할 근거가 된다.

구성요소 기술 게이트를 통과해도 출품 확정은 아니다. `review_proxy_reduction`은 실제 시간 측정이 아니라 미해결 단서와 누락 확인 건수의 대리지표다. 자산 발견 재현율 1.000도 감사 대상 파일을 재귀 열거한 결과이지, 실제 미디어 자산 분류 성능이 아니다.

## ASSUMPTION과 한계

- 미디어 내용 설명은 `.rightsledger_observations.json`으로 미리 제공했다. 이미지·음성 이해는 검증하지 않았다.
- 합성 프로젝트를 만든 사람과 평가 설계자가 같아 데이터셋 편향 가능성이 있다.
- 하이브리드 성능은 로컬 임베딩 관계 연결만 측정했다. 범용 LLM 원시 출력 5건은 확보했지만, 사후 예비 코딩 외의 독립 정확도 채점은 하지 않았다.
- C2PA 서명 검증과 SPDX 호환성 판단은 범위 밖이다.
- 실제 사용자 수동 감사 시간은 아직 측정하지 않았다.

## 다음 결정 조건

1. 독립 작성 프로젝트 5개에서 같은 임계값을 고정한 채 블라인드 재시험한다.
2. 확보한 범용 생성형 LLM 체크리스트를 독립 평가자가 블라인드 채점한다.
3. 사람이 기준선과 하이브리드 결과를 검증 완료하는 시간을 교차 측정한다.
4. 실제 시간 감소가 30% 미만이면 `DEC-010`에 따라 탈락시키고, 50% 이상이어야 전체 통과로 본다.
5. C2PA 읽기 사례와 실제 이미지·음원 추출은 별도 기술 스파이크로 검증한다.
"""
    (RESULTS / "experiment_report_2026-09-04.md").write_text(report, encoding="utf-8")
    print(f"technical_verdict={comparison['technical_verdict']} overall_verdict={comparison['overall_verdict']}")


def self_check() -> None:
    if not TRUTH.exists():
        generate()
    truth_files = sorted(TRUTH.glob("CASE-*.json"))
    assert len(truth_files) == 5
    truths = [json.loads(path.read_text(encoding="utf-8")) for path in truth_files]
    assert all(len(item["assets"]) == 15 for item in truths)
    assert sum(len(item["assets"]) for item in truths) == 75
    assert sum(len(item["missing_evidence"]) for item in truths) == 4
    for truth in truths:
        project = CASES / truth["case_id"] / "project"
        actual_paths = {
            path.relative_to(project).as_posix()
            for path in project.rglob("*")
            if path.is_file() and path.name != OBSERVATIONS
        }
        assert actual_paths == set(truth["assets"]), truth["case_id"]
        for relation in truth["relations"]:
            assert relation["from"] in actual_paths
            assert relation["to"] in actual_paths
    for mode in ("deterministic", "hybrid"):
        result_path = RESULTS / f"{mode}_predictions.jsonl"
        if not result_path.exists():
            continue
        predictions = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines()]
        assert len(predictions) == 5
        for prediction in predictions:
            project = CASES / prediction["case_id"] / "project"
            inventory = {item["path"]: item["sha256"] for item in prediction["inventory"]}
            truth = json.loads((TRUTH / f"{prediction['case_id']}.json").read_text(encoding="utf-8"))
            assert set(inventory) == set(truth["assets"])
            assert all(inventory[path] == sha256(project / path) for path in inventory)
    assert baseline_prompt_text()
    assert final_content("hidden trace</think>\n\nfinal answer") == ("final answer", True)
    assert final_content("final answer") == ("final answer", False)
    for spec in specs():
        dossier, paths = project_dossier(spec["case_id"])
        assert len(paths) == 15
        assert OBSERVATIONS not in dossier
        assert "ground_truth" not in dossier
    baseline_path = RESULTS / "general_llm_raw.jsonl"
    if baseline_path.exists():
        records = [json.loads(line) for line in baseline_path.read_text(encoding="utf-8").splitlines()]
        assert len(records) == 5
        assert len({item["case_id"] for item in records}) == 5
        assert len({item["prompt_sha256"] for item in records}) == 1
        assert all(len(item["input_paths"]) == 15 for item in records)
        assert all(OBSERVATIONS not in item["input_paths"] for item in records)
    control = predict_case("CASE-001", "deterministic", None)
    metrics = evaluate([control])
    assert metrics["asset_discovery"]["recall"] == 1.0
    assert metrics["relations"]["recall"] == 1.0
    assert metrics["legal_conclusion_count"] == 0
    print("self_check=pass cases=5 assets=75 intentional_missing=4 control_relation_recall=1.0")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("generate")
    subparsers.add_parser("self-check")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--mode", choices=("deterministic", "hybrid"), required=True)
    run_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    baseline_parser = subparsers.add_parser("llm-baseline")
    baseline_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    subparsers.add_parser("compare")
    args = parser.parse_args()

    if args.command == "generate":
        generate()
    elif args.command == "self-check":
        self_check()
    elif args.command == "run":
        run(args.mode, args.ollama_url)
    elif args.command == "llm-baseline":
        run_llm_baseline(args.ollama_url)
    else:
        compare()


if __name__ == "__main__":
    main()
