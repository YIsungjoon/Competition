# RightsLedger C2PA 스파이크

RightsLedger가 C2PA 매니페스트의 부재·정상·손상을 구분할 수 있는지 최소 범위로 검증한다.

## 고정 표본

공식 `c2pa-org/public-testfiles` 저장소의 `legacy/1.4/image/jpeg`에서 세 파일만 사용한다.

| 파일 | 공식 기대 상태 | SHA-256 |
|---|---|---|
| `adobe-20220124-A.jpg` | Content Credentials 없음 | `f999fd78bfe8a83c96e468a078830ba94485bc1bc6fd086fb94a43bd29dd0f23` |
| `adobe-20220124-C.jpg` | 매니페스트 있음, 테스트 인증서 | `75a8da33f6eaf1e16bf3b42cd78913b22b2e6a671fda217a508b1ba4230ce864` |
| `adobe-20220124-E-sig-CA.jpg` | 잘못된 서명 | `0d4c2774f1b7e94b9613bb952b0a76b6a178d22ac6d206d257d2af1376cbbff2` |

원본 저장소의 `README.md`와 `LICENSE` 사본도 `samples/raw/`에 보존했다. 표본 라이선스는 저장된 원본 `LICENSE`를 따른다.

## 실행

```bash
python3 06_experiments/rightsledger_c2pa/run_spike.py
python3 06_experiments/rightsledger_c2pa/run_spike.py --check
```

결과는 `results/`에 저장한다. 원시 도구 출력과 종료 코드, 요약, 보고서, 입력·출력 SHA-256을 모두 남긴다.

## 해석 경계

C2PA 매니페스트 무결성, 서명자 신뢰, 라이선스 증거는 서로 다른 축이다. 유효한 매니페스트를 저작권 보유 또는 이용 허락으로 해석하지 않는다.
