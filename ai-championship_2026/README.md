# Wanted AI Championship 2026 프로젝트

이 저장소는 출품 주제 탐색부터 최종 제출물까지의 자료와 판단 근거를 재현 가능하게 보관한다.

## 현재 단계

- 단계: `IDEA-051 사진이 묻는 하루` 제출용 MVP 빌드 완료, 서버 키·실제 사진 검증·배포 대기
- 기준일: 2026-09-14 (Asia/Seoul)
- 참가 접수 마감: 2026-09-18
- 과제 제출 마감: 2026-09-20
- 현재 출품 개발 1순위는 사용자 제안 `IDEA-051 사진이 묻는 하루`다. 사진 선택, 기억 질문 3개, 답변, 문장별 사진·사용자 근거가 있는 기록까지 서비스 코드와 브라우저 흐름을 구현했다. 샘플·근거 검사·프로덕션 빌드는 통과했지만 서버 키가 없어 실제 모델 호출과 프로덕션 배포는 아직 하지 않았다. 따라서 `작동하는 AI 서비스`가 아니라 `실제 모델 검증 직전의 배포 후보`로 기록한다.

## 현재 자료 규모

- 등록 출처: 99건
- Google Trends 평균 관심도 관찰: 105건
- 연관검색 기록: 83건 (판단 사용 79건, 오염으로 제외 4건)
- 아이디어 후보: 51개
- 2단계 비교 후보: 12개
- 24시간 검증 후보: 3개 (`IDEA-033`, `IDEA-051`, `IDEA-050`)
- 완료한 기술 스파이크: 2개 (`IDEA-033` 관계 연결, C2PA 읽기·검증 구성요소)
- 완료한 생성형 기준선: 10건 (`qwen3:4b`, 기존 입력 5건 + 공통입력 5건, 정식 블라인드 채점 전)
- 작동하는 MVP: 1개 (`RightsLedger 0.1`, 로컬·무저장) + 배포 후보 1개 (`사진이 묻는 하루`, 실제 AI 키 대기)
- 조건부 예비 1순위: `IDEA-004`
- 현재 원칙: 특정 도메인에 가산점을 주지 않고 문제 기능과 사용자 상황을 교차 탐색

## 어디서 시작할지

1. [파일·자료·의사결정 관리 기준](00_governance/FDS.md)
2. [작업 로그](00_governance/work_log.md)
3. [대회 핵심 요약](01_brief/competition_brief.md)
4. [AI 서비스 판단 기준](01_brief/ai_service_definition.md)
5. [Google Trends 조사 기록](02_research/google_trends/research_log_2026-09-03.md)
6. [아이디어 백로그](03_ideas/idea_backlog.md)
7. [교차도메인 확장 후보](03_ideas/cross_domain_expansion.md)
8. [문제 기능 중심 조사 지도](02_research/problem_space/problem_archetype_map.md)
9. [의사결정 로그](04_decisions/decision_log.md)
10. [사용자 아이디어 목록](03_ideas/user_ideas.md)
11. [IDEA-051 사진 기반 대화형 회고](03_ideas/concepts/IDEA-051_photo_reflection_journal.md)
12. [51개 후보 1차 점수 데이터](03_ideas/screening/phase1_scores_2026-09-03.jsonl)
13. [1차 경쟁·대체재 조사](02_research/competitive/phase1_shortlist_quick_scan_2026-09-03.md)
14. [10개 압축 결과와 다음 검증](03_ideas/screening/phase1_shortlist_2026-09-03.md)
15. [2단계 평가·탈락 프로토콜](03_ideas/screening/phase2_protocol_2026-09-03.md)
16. [12개 후보 심층 반증 조사](02_research/competitive/phase2_deep_scan_2026-09-03.md)
17. [2단계 점수 원문](03_ideas/screening/phase2_scores_2026-09-03.jsonl)
18. [상위 3개와 17일 실행안](03_ideas/screening/phase2_top3_2026-09-03.md)
19. [RightsLedger 구성요소 실험 결과](06_experiments/rightsledger_24h/results/experiment_report_2026-09-04.md)
20. [RightsLedger 독립 블라인드·시간 검증 절차 v2](06_experiments/rightsledger_24h/blind_validation_protocol_v2_2026-09-07.md)
21. [범용 LLM 기준선 예비 검토](06_experiments/rightsledger_24h/results/general_llm_preliminary_review_2026-09-04.md)
22. [범용 LLM 모델 선택 근거](02_research/model_selection/rightsledger_baseline_model_2026-09-04.md)
23. [C2PA 읽기·검증 스파이크](06_experiments/rightsledger_c2pa/results/c2pa_spike_report_2026-09-04.md)
24. [공통입력 범용 LLM 민감도 분석](06_experiments/rightsledger_24h/results/general_llm_shared_preliminary_review_2026-09-07.md)
25. [독립 데이터·검토자 전달 패키지](06_experiments/rightsledger_blind/README.md)
26. [RightsLedger 1인 형성평가 절차](06_experiments/rightsledger_solo/solo_validation_protocol_2026-09-07.md)
27. [RightsLedger 로컬 MVP 실행](05_deliverables/rightsledger_mvp/README.md)
28. [SOLO-001 참여자 카드](06_experiments/rightsledger_solo/SOLO-001_participant_card.md)
29. [IDEA-051 출품 MVP 계약](05_deliverables/photo_reflection_mvp/MVP_CONTRACT.md)
30. [IDEA-051 비전 모델·개인정보 결정](02_research/model_selection/idea_051_vision_model_decision_2026-09-07.md)
31. [PHOTO-P01 대화형 형성평가 카드](06_experiments/photo_reflection_24h/PHOTO-P01_session_card.md)
32. [IDEA-051 MVP 구현·검증 보고서](05_deliverables/photo_reflection_mvp/BUILD_REPORT_2026-09-14.md)
33. [IDEA-051 웹 서비스 실행 안내](05_deliverables/photo_reflection_mvp/site/README.md)

## 폴더 역할

| 경로 | 역할 |
|---|---|
| `00_governance/` | 파일 규칙, 출처 목록, 작업 이력 |
| `01_brief/` | 대회 조건과 프로젝트의 공통 판단 기준 |
| `02_research/` | 외부 조사 원본·관찰값·분석 |
| `03_ideas/` | 후보 아이디어와 평가 |
| `04_decisions/` | 선택·보류·폐기의 근거 |
| `05_deliverables/` | 제출 가능한 최종 산출물 |
| `06_experiments/` | 합성·블라인드 데이터, 실행 코드, 원시 예측, 지표와 실험 절차 |

## 상태 표기

- `FACT`: 출처에서 직접 확인한 사실
- `OBSERVATION`: 수치나 화면에서 직접 읽은 관찰값
- `INTERPRETATION`: 관찰값에 대한 해석
- `DECISION`: 프로젝트에서 채택한 선택
- `ASSUMPTION`: 아직 검증되지 않은 가정
