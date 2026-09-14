## 출처·라이선스·구매증빙·AI 생성 기록 체크리스트

다음은 제출 전 확인해야 할 핵심 증빙 사항입니다. 각 입력 자산에 대한 **현재 존재하는 증빙**과 **빠진 것으로 보이는 증빙**을 명시했습니다. 연결 근거가 약한 경우 `확인 필요`로 표시했습니다.

---

### 1. `media/img_1042.png` (neon-lit evening food market photo)
- **현재 존재하는 증빙**:
  - `evidence/source/night_market_origin.txt`: 원본 주소: 네온 간판이 빛나는 야시장 골목의 거리 사진
  - `evidence/license/street_photo_permission.txt`: Attribution license for the night street food market photograph
- **빠진 증빙**:
  - 없음

> ✅ **확인 완료**: 사진의 원본 주소와 라이선스 증빙이 모두 제공됨. `lineage/reel_notes.md`에서 "neon-lit evening food market scene photographed at street level"으로 명시됨.

---

### 2. `audio/track_final.wav` (purchased hand-drum rhythm)
- **현재 존재하는 증빙**:
  - `evidence/receipt/rhythm_order.txt`: Receipt for the energetic hand-drum loop used in the weekend reel
  - `evidence/license/percussion_terms.txt`: Commercial synchronization license for the upbeat percussion recording
- **빠진 증빙**:
  - 없음

> ✅ **확인 완료**: 구매 증빙과 라이선스가 모두 제공됨. `lineage/reel_notes.md`에서 "energetic purchased hand-drum rhythm"으로 명시됨.

---

### 3. `src/lib_a.js` (bar chart component)
- **현재 존재하는 증빙**:
  - `evidence/license/chart_mit.txt`: MIT license notice for the adapted OpenPlot Mini chart component
  - `evidence/source/chart_upstream.txt`: Upstream repository for the OpenPlot Mini bar-chart component
- **빠진 증빙**:
  - 없음

> ✅ **확인 완료**: 오픈소스 라이선스와 원본 코드 저장소 증빙이 모두 제공됨. `lineage/reel_notes.md`에서 "adapted OpenPlot Mini bar chart component"로 명시됨.

---

### 4. `generated/voice_take.wav` (synthetic Korean narrator)
- **현재 존재하는 증빙**:
  - `evidence/prompt/narration_prompt.txt`: 생성 프롬프트: 주말 야시장으로 초대하는 밝은 한국어 여성 내레이션
- **빠진 증빙**:
  - AI 생성 기록 (예: 사용된 모델, 생성 시간, 파라미터 등) → **확인 필요**

> ⚠️ **확인 필요**: 프롬프트는 제공되었으나, 실제 AI 생성 과정의 기록(모델 이름, 생성 시간 등)이 없음. `lineage/reel_notes.md`에서 "synthetic Korean weekend-market invitation voice"로 명시되었으나, 생성 기록이 문서화되지 않음.

---

### 5. `deliverables/reel_v7.mp4` (final output)
- **현재 존재하는 증빙**:
  - `lineage/reel_notes.md`: Output: deliverables/reel_v7.mp4 (4가지 입력 자산 명시)
- **빠진 증빙**:
  - 없음

> ✅ **확인 완료**: 최종 출력물에 대한 입력 자산 연결 기록이 완전히 제공됨.

---

### 📌 핵심 확인 포인트
1. **AI 생성 기록**은 `generated/voice_take.wav`에 대해 **확인 필요**입니다. 프롬프트는 제공되었으나, 실제 생성 과정의 기록(모델, 시간 등)이 없어 제출 전 추가 검증이 필요합니다.
2. 모든 입력 자산에 대한 **라이선스·구매 증빙**은 완전히 제공됨. `evidence/` 폴더 내 파일이 각 자산과 일치하는 것으로 확인됨.
3. `lineage/reel_notes.md`는 모든 입력 자산을 명확히 연결해 제출 전 검증을 완료할 수 있도록 도움을 줍니다.

> 💡 **추가 권장**: AI 생성 기록을 추가로 기록해 `generated/voice_take.wav`의 출처를 명확히 하면 제출 시 더 안전한 상태로 납품할 수 있습니다.