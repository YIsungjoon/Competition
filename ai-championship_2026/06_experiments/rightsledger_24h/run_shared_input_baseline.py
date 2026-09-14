#!/usr/bin/env python3
"""Run the frozen Qwen baseline with the same asset declarations as RightsLedger."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from datetime import datetime
from pathlib import Path

import experiment as core


RUN_ID = "EXP-RL-20260904-03"
ROOT = Path(__file__).resolve().parent
INPUT_DIR = core.RESULTS / "general_llm_shared_inputs"
OUTPUT_DIR = core.RESULTS / "general_llm_shared_outputs"
CASE_RECORD_DIR = core.RESULTS / "general_llm_shared_raw_cases"
RAW_PATH = core.RESULTS / "general_llm_shared_raw.jsonl"
METRICS_PATH = core.RESULTS / "general_llm_shared_run_metrics.json"
MANIFEST_PATH = ROOT / "run_manifest_general_llm_shared_2026-09-04.json"


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def request_json(url: str, payload: dict | None = None, timeout: int = 10) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def case_input(case_id: str, prompt: str) -> tuple[str, str]:
    dossier, _ = core.project_dossier(case_id)
    observation_path = core.CASES / case_id / "project" / core.OBSERVATIONS
    observations = observation_path.read_text(encoding="utf-8").strip()
    content = (
        f"{prompt}\n\n## 프로젝트 입력\n\n{dossier}\n\n"
        "## 공통 자산 선언\n\n"
        "다음 선언은 비교하는 두 조건에 동일하게 제공됩니다. 관계·누락 정답은 포함하지 않습니다.\n\n"
        f"```json\n{observations}\n```"
    )
    return content, core.sha256(observation_path)


def run(base_url: str) -> None:
    prompt = core.baseline_prompt_text()
    prompt_sha = text_sha256(prompt)
    runner_sha = core.sha256(Path(__file__))
    core_sha = core.sha256(Path(core.__file__))
    runtime_version = request_json(base_url.rstrip("/") + "/api/version").get("version")
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CASE_RECORD_DIR.mkdir(parents=True, exist_ok=True)
    records = []

    for spec in core.specs():
        case_id = spec["case_id"]
        content, observation_sha = case_input(case_id, prompt)
        input_path = INPUT_DIR / f"{case_id}.md"
        if input_path.exists() and input_path.read_text(encoding="utf-8") != content:
            raise SystemExit(f"Refusing changed resumed input: {case_id}")
        input_path.write_text(content, encoding="utf-8")
        input_sha = core.sha256(input_path)
        output_path = OUTPUT_DIR / f"{case_id}.md"
        record_path = CASE_RECORD_DIR / f"{case_id}.json"

        if record_path.exists():
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if record["input_sha256"] != input_sha or record["runner_sha256"] != runner_sha:
                raise SystemExit(f"Refusing incompatible resumed record: {case_id}")
            checklist, _ = core.final_content(record["raw_response"]["message"]["content"])
            if not output_path.exists():
                output_path.write_text(checklist, encoding="utf-8")
            if core.sha256(output_path) != record["output_sha256"]:
                raise SystemExit(f"Output hash mismatch: {case_id}")
            print(f"case={case_id} resumed=true")
            records.append(record)
            continue

        payload = {
            "model": core.BASELINE_MODEL,
            "messages": [{"role": "user", "content": content}],
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0,
                "seed": core.BASELINE_SEED,
                "num_ctx": core.BASELINE_CONTEXT,
            },
        }
        raw_response = request_json(base_url.rstrip("/") + "/api/chat", payload, timeout=600)
        checklist, stripped = core.final_content(raw_response.get("message", {}).get("content", ""))
        if not checklist:
            raise SystemExit(f"Empty checklist: {case_id}")
        output_path.write_text(checklist, encoding="utf-8")
        record = {
            "run_id": RUN_ID,
            "case_id": case_id,
            "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "model": core.BASELINE_MODEL,
            "model_local_id": "359d7dd4bcda",
            "options": {
                "temperature": 0,
                "seed": core.BASELINE_SEED,
                "num_ctx": core.BASELINE_CONTEXT,
                "think": False,
            },
            "prompt_sha256": prompt_sha,
            "shared_observation_sha256": observation_sha,
            "input_sha256": input_sha,
            "output_sha256": core.sha256(output_path),
            "runner_sha256": runner_sha,
            "core_sha256": core_sha,
            "stripped_inline_thinking": stripped,
            "raw_response": raw_response,
        }
        core.dump_json(record_path, record)
        records.append(record)
        print(f"case={case_id} resumed=false checklist_chars={len(checklist)}")

    records.sort(key=lambda item: item["case_id"])
    RAW_PATH.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records),
        encoding="utf-8",
    )
    metrics = {
        "run_id": RUN_ID,
        "mode": "general_llm_checklist_shared_input",
        "model": core.BASELINE_MODEL,
        "case_count": len(records),
        "inference_duration_seconds": sum(
            item["raw_response"].get("total_duration", 0) for item in records
        ) / 1_000_000_000,
        "responses_requiring_inline_thinking_strip": sum(
            item["stripped_inline_thinking"] for item in records
        ),
        "human_review_time_seconds": None,
        "accuracy_metrics": None,
        "shared_input_fields": ["path", "description", "origin_type"],
    }
    core.dump_json(METRICS_PATH, metrics)
    tracked = (
        sorted(INPUT_DIR.glob("*.md"))
        + sorted(OUTPUT_DIR.glob("*.md"))
        + sorted(CASE_RECORD_DIR.glob("*.json"))
        + [RAW_PATH, METRICS_PATH]
    )
    manifest = {
        "run_id": RUN_ID,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "runtime": {"name": "Ollama", "version": runtime_version, "external_data_transmission": False},
        "model": {"name": core.BASELINE_MODEL, "local_model_id": "359d7dd4bcda"},
        "runner_sha256": runner_sha,
        "core_sha256": core_sha,
        "prompt_body_sha256": prompt_sha,
        "files_sha256": {str(path.relative_to(ROOT)): core.sha256(path) for path in tracked},
        "result": metrics,
        "comparison_boundary": "Same synthetic cases and same asset declarations; still not independent or blinded.",
    }
    core.dump_json(MANIFEST_PATH, manifest)
    print(f"complete cases={len(records)} inference_seconds={metrics['inference_duration_seconds']:.3f}")


def check() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    errors = []
    if manifest["runner_sha256"] != core.sha256(Path(__file__)):
        errors.append("runner changed")
    if manifest["core_sha256"] != core.sha256(Path(core.__file__)):
        errors.append("core changed")
    for relative, expected in manifest["files_sha256"].items():
        path = ROOT / relative
        if not path.is_file() or core.sha256(path) != expected:
            errors.append(f"hash mismatch: {relative}")
    inputs = sorted(INPUT_DIR.glob("*.md"))
    if len(inputs) != 5 or not all("## 공통 자산 선언" in path.read_text(encoding="utf-8") for path in inputs):
        errors.append("shared inputs missing")
    if errors:
        raise SystemExit("FAIL: " + "; ".join(errors))
    print("PASS: five shared inputs and all recorded hashes are valid")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    check() if args.check else run(args.ollama_url)


if __name__ == "__main__":
    main()
