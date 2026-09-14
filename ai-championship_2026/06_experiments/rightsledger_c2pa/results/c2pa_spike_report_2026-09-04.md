# RightsLedger C2PA 읽기·검증 스파이크

- 실험 ID: `EXP-RL-C2PA-20260904-01`
- 실행일: 2026-09-04 (Asia/Seoul)
- 도구: `c2patool 0.27.17`
- 표본: C2PA 공식 공개 테스트 JPEG 3개
- 결과: **3개 기대 상태를 모두 구분함**

## 질문

RightsLedger가 파일에서 C2PA 매니페스트의 부재, 무결성 통과, 서명 손상을 서로 다른 상태로 읽어낼 수 있는가?

## 결과

| 사례 | 기대 | 관찰 | 핵심 검증 코드 | 판정 |
|---|---|---|---|---|
| C2PA-ABSENT | `no_manifest` | `no_manifest` | 없음 | 일치 |
| C2PA-VALID | `manifest_valid_with_untrusted_signer` | `manifest_valid_with_untrusted_signer` | `signingCredential.untrusted` | 일치 |
| C2PA-INVALID-SIGNATURE | `manifest_invalid` | `manifest_invalid` | `claimSignature.mismatch`, `signingCredential.untrusted` | 일치 |

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
