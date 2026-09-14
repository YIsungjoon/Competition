# 제출 또는 납품 전 확인 필수 체크리스트

이 체크리스트는 제공된 프로젝트 파일 경로와 내용만을 기반으로 작성되었습니다. **법적 결론을 내리지 않으며**, 연결 근거가 약한 경우 `확인 필요`로 표시했습니다. 모든 항목은 실제 파일 경로와 내용을 직접 참조해 작성했습니다.

---

## 1. 출처 확인 (Sources)

### 1.1 아코스틱 기타 인트로 (media/a_17.wav)
- **현재 증빙**:  
  - `evidence/receipt/guitar_standard_order.txt` (구매증빙)  
  - `evidence/license/guitar_standard_license.txt` (라이선스)  
- **빠진 증빙**: 없음  
- **근거**: `lineage/episode_cue.md`에서 "the selected standard-tempo gentle acoustic guitar intro"로 사용됨. `media/a_17.wav`의 설명 "standard-tempo gentle acoustic guitar recording selected for the podcast intro"와 일치.

### 1.2 전자 로고 스티그 (generated/music_sting.wav)
- **현재 증빙**:  
  - `evidence/prompt/sting_prompt.txt` (AI 생성 프롬프트)  
  - `evidence/model_terms/sting_model_terms.txt` (AI 모델 용어)  
- **빠진 증빙**: 없음  
- **근거**: `lineage/episode_cue.md`에서 "the generated electronic three-note show logo"로 사용됨. `generated/music_sting.wav`의 설명 "short electronic three-note logo sting generated for the show"와 일치.

### 1.3 창업자 포트레이트 (media/photo_x.png)
- **현재 증빙**:  
  - `evidence/author/portrait_author.txt` (저작자 승인)  
- **빠진 증빙**: 구매증빙 없음 (사진은 직접 촬영된 것으로 보임)  
- **근거**: `media/photo_x.png`의 설명 "founder portrait photographed beside a window in soft daylight"와 `evidence/author/portrait_author.txt`의 내용 "Team authorship statement for the founder portrait shot"이 일치.

---

## 2. 라이선스 확인 (Licenses)

### 2.1 아코스틱 기타 인트로 라이선스
- **현재 증빙**: `evidence/license/guitar_standard_license.txt` (포스터同步 라이선스)  
- **빠진 증빙**: 없음  
- **근거**: `evidence/license/guitar_standard_license.txt`에서 "Podcast synchronization license for the selected standard-tempo gentle guitar take"로 명시됨.

### 2.2 전자 로고 스티그 라이선스
- **현재 증빙**: `evidence/model_terms/sting_model_terms.txt` (모델 용어)  
- **빠진 증빙**: 명확한 라이선스 문서 없음  
- **근거**: `evidence/model_terms/sting_model_terms.txt`에서 "Terms snapshot for the audio model"으로, 모델의 사용 조건을 설명하지만 실제 라이선스 문서가 아님. `lineage/episode_cue.md`에서 스티그가 생성된 과정을 기록하지만, 라이선스 문서가 없음.

---

## 3. 구매증빙 확인 (Purchase Proofs)

### 3.1 아코스틱 기타 인트로 구매증빙
- **현재 증빙**: `evidence/receipt/guitar_standard_order.txt` (주문 증빙)  
- **빠진 증빙**: 없음  
- **근거**: `evidence/receipt/guitar_standard_order.txt`에서 "Order receipt for the standard-tempo acoustic guitar intro recording"로 명시됨.

### 3.2 전자 로고 스티그 구매증빙
- **현재 증빙**: 없음 (AI 생성물)  
- **빠진 증빙**: 없음  
- **근거**: `generated/music_sting.wav`는 AI 생성물로 구매가 필요하지 않음.

### 3.3 창업자 포트레이트 구매증빙
- **현재 증빙**: 없음 (직접 촬영)  
- **빠진 증빙**: 없음  
- **근거**: `media/photo_x.png`의 설명 "founder portrait photographed beside a window in soft daylight"에서 구매가 아닌 직접 촬영으로 명시됨.

---

## 4. AI 생성 기록 확인 (AI Generation Records)

### 4.1 전자 로고 스티그 생성 기록
- **현재 증빙**:  
  - `evidence/prompt/sting_prompt.txt` (프롬프트)  
  - `evidence/model_terms/sting_model_terms.txt` (모델 용어)  
- **빠진 증빙**: 없음  
- **근거**: `lineage/episode_cue.md`에서 "the generated electronic three-note show logo"로 사용됨. `evidence/prompt/sting_prompt.txt`에서 "Prompt: a concise electronic three-note sonic logo for a podcast"로 명시됨.

### 4.2 기타 생성 기록
- **현재 증빙**: 없음  
- **빠진 증빙**: 없음  
- **근거**: 프로젝트 내 다른 AI 생성물이 없음.

---

## 5. 기타 확인 사항

### 5.1 최종 배포물 (deliverables/podcast_ep1.wav)
- **현재 증빙**: `lineage/episode_cue.md` (출력 경로 및 입력 자산)  
- **빠진 증빙**: 없음  
- **근거**: `lineage/episode_cue.md`에서 "Output: deliverables/podcast_ep1.wav"로 명시됨.

### 5.2 미사용 자산 (media/a_18.wav)
- **현재 증빙**: `media/a_18.wav` (slower alternate guitar recording)  
- **빠진 증빙**: 없음  
- **근거**: `media/a_18.wav`의 설명 "slower alternate gentle acoustic guitar recording not selected for the intro"로 미사용 자산임을 명시.

---

> **주의**: 이 체크리스트는 제공된 파일 경로와 내용만을 기반으로 작성되었습니다.  
> - **연결 근거가 약한 경우**: `2.2 전자 로고 스티그 라이선스` 항목에서 "명확한 라이선스 문서 없음"은 모델 용어가 실제 라이선스 문서가 아님을 확인할 수 없음 → `확인 필요`로 표시.  
> - **법적 결론은 내리지 않음**: 모든 항목은 증빙 상태와 빠진 부분만 기술했으며, "권리가 있다", "침해다" 등은 포함하지 않음.  
> - **사용자 확인 권장**: 실제 프로젝트에서 사용되는 자산과 라이선스 조건을 다시 검토해 주세요.
