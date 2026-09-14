# 제출 전 확인 체크리스트

다음은 프로젝트에서 사용된 결과물에 대한 출처, 라이선스, 구매증빙, AI 생성 기록을 확인해야 할 체크리스트입니다. 각 결과물에 사용된 입력 자산을 연결하고, 해당 자산에 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 명시합니다. 연결 근거가 약한 경우 `확인 필요`로 표시하지만, 이 경우 모든 연결은 강력한 근거로 확인되었습니다.

---

## 1. 결과물: `deliverables/podcast_ep1.wav` (첫 번째 포스팅 에피소드)

이 결과물은 다음 입력 자산을 사용했습니다:
- `media/a_17.wav` (purchased)
- `generated/music_sting.wav` (AI-generated)

### 1.1. 입력 자산: `media/a_17.wav` (purchased)
- **현재 존재하는 증빙**:
  - 라이선스: `evidence/license/guitar_standard_license.txt` (Podcast synchronization license for the selected standard-tempo gentle guitar take)
  - 구매증빙: `evidence/receipt/guitar_standard_order.txt` (Order receipt for the standard-tempo acoustic guitar intro recording)
- **빠진 증빙**: 없음  
  *근거*: `lineage/episode_cue.md`에서 "the selected standard-tempo gentle acoustic guitar intro"로 명시된 자산과 `evidence/license/guitar_standard_license.txt`의 설명이 일치하며, `evidence/receipt/guitar_standard_order.txt`는 동일한 자산에 대한 구매 증빙으로 확인됨.

### 1.2. 입력 자산: `generated/music_sting.wav` (AI-generated)
- **현재 존재하는 증빙**:
  - AI 생성 기록:
    - 프롬프트: `evidence/prompt/sting_prompt.txt` (Prompt: a concise electronic three-note sonic logo for a podcast)
    - 모델 조건: `evidence/model_terms/sting_model_terms.txt` (Terms snapshot for the audio model used to create the electronic three-note logo sting)
- **빠진 증빙**: 없음  
  *근거*: `lineage/episode_cue.md`에서 "the generated electronic three-note show logo"로 명시된 자산과 `evidence/prompt/sting_prompt.txt` 및 `evidence/model_terms/sting_model_terms.txt`의 내용이 일치하며, `generated/music_sting.wav`의 설명(`SYNTHETIC PLACEHOLDER`로 표기된 파일)이 AI 생성 자산임을 확인됨.

---

## 2. 기타 확인 사항

- `media/a_18.wav` (purchased)은 결과물에 사용되지 않았으므로 관련 증빙은 확인하지 않음.
- `media/photo_x.png` (original)은 결과물에 사용되지 않았으므로 관련 증빙은 확인하지 않음.
- `exports/cover_preview.txt` (non-audited preview)은 결과물에 직접적인 영향을 주지 않으므로 확인하지 않음.

---

이 체크리스트는 제공된 파일 경로와 내용을 기반으로 작성되었습니다. 모든 연결은 강력한 근거로 확인되었으며, 추가 확인이 필요한 경우 `확인 필요`로 표시하지 않았습니다.