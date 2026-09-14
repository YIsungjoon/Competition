# RightsLedger 독립 검증 전달 패키지

이 폴더는 독립 데이터 작성자와 검토자가 현재 구현이나 기존 정답을 보지 않고 [블라인드 프로토콜 v2](../rightsledger_24h/blind_validation_protocol_v2_2026-09-07.md)를 실행하기 위한 최소 전달물이다. 독립 작성자에게는 전체 저장소 링크가 아니라 이 폴더의 필요한 템플릿과 검사기만 복사해 전달한다.

## 역할별 절차

### 독립 데이터 작성자

1. 이 저장소 밖의 새 폴더에 아래 구조를 만든다.
2. `B01`~`B05` 프로젝트를 서로 다른 맥락으로 작성한다. 현재 `CASE-001~005`는 열어보지 않는다.
3. `shared_intake_template.json`으로 공통 선언을, `blind_case_truth_template_v2.json`으로 정답을 작성한다.
4. `validate_intake.py`를 자신의 묶음에 실행한다.
5. 운영자에게 `projects/`, `shared/`, `validation_receipt.json`만 전달한다. `truth/`는 10개 검토 제출물이 해시로 잠길 때까지 보내지 않는다.

```text
author_bundle/
  projects/B01/project/...
  projects/B02/project/...
  ...
  shared/B01.json
  shared/B02.json
  ...
  truth/B01.json
  truth/B02.json
  truth/c2pa/...
```

```bash
python3 validate_intake.py /path/to/author_bundle --receipt /path/to/validation_receipt.json
```

실제 개인정보나 권리가 불명확한 자료를 쓰지 않는다. 직접 만든 합성 자료, 명시적으로 허용된 공개 자료, 테스트 전용 자산만 사용하고 원출처와 이용조건은 정답 묶음에 남긴다.

### 실험 운영자

정답 폴더가 전달되지 않았는지 먼저 확인한다. 공통 선언과 프로젝트 파일을 두 조건에 동일하게 투입하고 입력·출력·코드 해시를 저장한다. 임계값이나 프롬프트는 실행 중 바꾸지 않는다.

### 검토자

`assignments.csv` 순서대로 자신에게 배정된 5건만 본다. 조건의 출력을 열기 직전에 시작 시각을 기록하고, `review_submission_template.json`에 최종 관계·누락·잘못된 경로·금지 결론을 저장한다.

## 독립 작성자에게 보낼 짧은 요청문

> AI 프로젝트 자산 감사 실험용 가상 프로젝트 5개를 만들어 주세요. 기존 사례와 구현은 보지 않고, 제공한 v2 계약에 따라 프로젝트당 입력 자산 15개·결과물 1개 이상·의도적 증거 누락 2개 이상을 구성해 주세요. 프로젝트와 공통 자산 선언만 먼저 전달하고 정답은 10개 검토가 끝날 때까지 보관해 주세요.

## 현재 상태

템플릿·배정표·자동 인입 검사는 준비됐다. 실제 독립 데이터와 두 검토자는 아직 확보되지 않았다.
