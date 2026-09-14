#!/usr/bin/env python3
"""Run and preserve the minimal RightsLedger C2PA read/validation spike."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SAMPLE_DIR = ROOT / "samples" / "raw"
RESULT_DIR = ROOT / "results"
SUMMARY_PATH = RESULT_DIR / "summary_2026-09-04.json"
REPORT_PATH = RESULT_DIR / "c2pa_spike_report_2026-09-04.md"
MANIFEST_PATH = ROOT / "run_manifest_2026-09-04.json"

SAMPLES = (
    {
        "case_id": "C2PA-ABSENT",
        "filename": "adobe-20220124-A.jpg",
        "expected_state": "no_manifest",
        "sha256": "f999fd78bfe8a83c96e468a078830ba94485bc1bc6fd086fb94a43bd29dd0f23",
    },
    {
        "case_id": "C2PA-VALID",
        "filename": "adobe-20220124-C.jpg",
        "expected_state": "manifest_valid_with_untrusted_signer",
        "sha256": "75a8da33f6eaf1e16bf3b42cd78913b22b2e6a671fda217a508b1ba4230ce864",
    },
    {
        "case_id": "C2PA-INVALID-SIGNATURE",
        "filename": "adobe-20220124-E-sig-CA.jpg",
        "expected_state": "manifest_invalid",
        "sha256": "0d4c2774f1b7e94b9613bb952b0a76b6a178d22ac6d206d257d2af1376cbbff2",
    },
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validation_codes(report: dict) -> list[str]:
    return sorted(
        {
            item.get("code", "")
            for item in report.get("validation_status", [])
            if isinstance(item, dict) and item.get("code")
        }
    )


def classify(returncode: int, stdout: str, stderr: str, report: dict | None) -> dict:
    if "No claim found" in f"{stdout}\n{stderr}":
        return {
            "observed_state": "no_manifest",
            "manifest_presence": "absent",
            "integrity_state": "not_applicable",
            "signer_trust_state": "not_applicable",
            "validation_state_raw": None,
            "validation_codes": [],
        }

    if report is None:
        return {
            "observed_state": "unparsed_tool_result",
            "manifest_presence": "unknown",
            "integrity_state": "unknown",
            "signer_trust_state": "unknown",
            "validation_state_raw": None,
            "validation_codes": [],
        }

    codes = validation_codes(report)
    raw_state = report.get("validation_state")
    presence = "present" if report.get("active_manifest") else "absent"
    trust = "untrusted" if "signingCredential.untrusted" in codes else "not_reported_untrusted"

    if presence == "present" and raw_state == "Invalid":
        observed = "manifest_invalid"
        integrity = "invalid"
    elif presence == "present" and raw_state == "Valid":
        observed = "manifest_valid_with_untrusted_signer" if trust == "untrusted" else "manifest_valid"
        integrity = "valid"
    else:
        observed = "manifest_state_unknown"
        integrity = "unknown"

    return {
        "observed_state": observed,
        "manifest_presence": presence,
        "integrity_state": integrity,
        "signer_trust_state": trust,
        "validation_state_raw": raw_state,
        "validation_codes": codes,
    }


def make_report(summary: dict) -> str:
    rows = []
    for sample in summary["samples"]:
        codes = ", ".join(f"`{code}`" for code in sample["validation_codes"]) or "없음"
        rows.append(
            f"| {sample['case_id']} | `{sample['expected_state']}` | "
            f"`{sample['observed_state']}` | {codes} | {'일치' if sample['expected_match'] else '불일치'} |"
        )

    return f"""# RightsLedger C2PA 읽기·검증 스파이크

- 실험 ID: `EXP-RL-C2PA-20260904-01`
- 실행일: 2026-09-04 (Asia/Seoul)
- 도구: `{summary['tool']['version']}`
- 표본: C2PA 공식 공개 테스트 JPEG 3개
- 결과: **3개 기대 상태를 모두 구분함**

## 질문

RightsLedger가 파일에서 C2PA 매니페스트의 부재, 무결성 통과, 서명 손상을 서로 다른 상태로 읽어낼 수 있는가?

## 결과

| 사례 | 기대 | 관찰 | 핵심 검증 코드 | 판정 |
|---|---|---|---|---|
{chr(10).join(rows)}

`C2PA-VALID`는 매니페스트 무결성 상태가 `Valid`였지만 테스트 인증서이므로 `signingCredential.untrusted`가 함께 보고됐다. `C2PA-INVALID-SIGNATURE`는 `Invalid`와 `claimSignature.mismatch`를 반환했다. 매니페스트가 없는 파일은 도구 종료 코드 1과 `No claim found`를 반환했다.

## 판단

- **구성요소 통과:** 이 실행 조건에서는 세 상태를 재현 가능하게 구분했다.
- **상태를 분리 저장:** `manifest_presence`, `integrity_state`, `signer_trust_state`, 원시 검증 코드를 별도 필드로 보존한다.
- **권리 판정 금지:** C2PA 무결성이나 서명자 신뢰는 저작권·라이선스 허락의 존재를 증명하지 않는다. RightsLedger의 영수증·라이선스·원출처 증거와 별도 축으로 취급한다.
- **최종 게이트 미완료:** 공식 고정 표본 3개에 대한 리더 스파이크일 뿐, 독립 작성 프로젝트·다른 포맷·실제 제작 파이프라인을 검증하지 않았다.

## 재현

```bash
python3 06_experiments/rightsledger_c2pa/run_spike.py
python3 06_experiments/rightsledger_c2pa/run_spike.py --check
```

원시 stdout·stderr·종료 코드와 파싱된 보고서는 `results/raw_*.json`에 저장했다. 파일 해시와 결과 해시는 `run_manifest_2026-09-04.json`에 있다.

## 출처와 한계

- `SRC-073`: c2pa-rs 공식 CLI 문서
- `SRC-074`: Homebrew c2patool 공식 formula
- `SRC-075`: C2PA 공식 공개 테스트 파일 저장소
- 표본은 공식 저장소의 `legacy/1.4` 호환성 자료이며 최신 C2PA 2.x 기능 범위를 대표하지 않는다.
- 테스트 인증서의 `untrusted`를 실제 배포 서명자의 불신 또는 권리 부재로 일반화하지 않는다.
"""


def run() -> None:
    executable = shutil.which("c2patool")
    if not executable:
        raise SystemExit("c2patool not found on PATH")

    version_process = subprocess.run(
        [executable, "-V"], capture_output=True, text=True, check=True
    )
    version = (version_process.stdout or version_process.stderr).strip()
    started_at = datetime.now().astimezone().isoformat(timespec="seconds")
    results = []

    for sample in SAMPLES:
        path = SAMPLE_DIR / sample["filename"]
        actual_sha = sha256(path)
        if actual_sha != sample["sha256"]:
            raise SystemExit(f"SHA-256 mismatch: {sample['filename']}")

        start = time.perf_counter()
        process = subprocess.run([executable, str(path)], capture_output=True, text=True)
        elapsed = time.perf_counter() - start
        try:
            parsed = json.loads(process.stdout)
        except json.JSONDecodeError:
            parsed = None

        classification = classify(process.returncode, process.stdout, process.stderr, parsed)
        record = {
            "case_id": sample["case_id"],
            "source_file": str(path.relative_to(ROOT)),
            "sha256": actual_sha,
            "expected_state": sample["expected_state"],
            **classification,
            "expected_match": classification["observed_state"] == sample["expected_state"],
            "duration_seconds": round(elapsed, 6),
            "command": [executable, str(path)],
            "returncode": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "parsed_report": parsed,
        }
        raw_path = RESULT_DIR / f"raw_{sample['case_id'].lower().replace('-', '_')}.json"
        write_json(raw_path, record)
        results.append({key: value for key, value in record.items() if key not in {"stdout", "stderr", "parsed_report"}})

    summary = {
        "experiment_id": "EXP-RL-C2PA-20260904-01",
        "started_at": started_at,
        "tool": {"path": executable, "version": version},
        "source": {
            "repository": "https://github.com/c2pa-org/public-testfiles",
            "fixture_path": "legacy/1.4/image/jpeg",
            "license_file": "samples/raw/LICENSE",
        },
        "samples": results,
        "all_expected_matched": all(item["expected_match"] for item in results),
        "interpretation_boundary": "C2PA state is provenance metadata evidence, not a copyright or license conclusion.",
    }
    write_json(SUMMARY_PATH, summary)
    REPORT_PATH.write_text(make_report(summary), encoding="utf-8")

    output_paths = sorted(RESULT_DIR.glob("raw_*.json")) + [SUMMARY_PATH, REPORT_PATH]
    manifest = {
        "experiment_id": summary["experiment_id"],
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tool": summary["tool"],
        "script_sha256": sha256(Path(__file__)),
        "input_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in sorted(SAMPLE_DIR.iterdir())
            if path.is_file()
        },
        "output_sha256": {
            str(path.relative_to(ROOT)): sha256(path) for path in output_paths
        },
        "all_expected_matched": summary["all_expected_matched"],
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"PASS: {len(results)} C2PA states matched; {REPORT_PATH.relative_to(ROOT)}")


def check() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    errors = []
    if not manifest.get("all_expected_matched"):
        errors.append("run did not match all expected states")
    if manifest.get("script_sha256") != sha256(Path(__file__)):
        errors.append("script hash changed after run")
    for group in ("input_sha256", "output_sha256"):
        for relative, expected in manifest.get(group, {}).items():
            path = ROOT / relative
            if not path.is_file() or sha256(path) != expected:
                errors.append(f"hash mismatch: {relative}")
    if errors:
        raise SystemExit("FAIL: " + "; ".join(errors))
    print("PASS: manifest flag and all recorded hashes are valid")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify the saved run without re-running c2patool")
    args = parser.parse_args()
    check() if args.check else run()


if __name__ == "__main__":
    main()
