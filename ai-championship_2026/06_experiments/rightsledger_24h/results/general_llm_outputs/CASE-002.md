# 제출 전 출처·라이선스·구매증빙·AI 생성 기록 체크리스트

다음과 같이 각 입력 자산에 대한 증빙을 확인하세요. 연결 근거가 약한 경우 `확인 필요`로 표시합니다.

## 1. Neon-lit evening food market scene (photographed at street level)

- **현재 증빙**:
  - `media/img_1042.png`: neon-lit evening food market photo
  - `evidence/source/night_market_origin.txt`: 원본 주소: 네온 간판이 빛나는 야시장 골목의 거리 사진
  - `evidence/license/street_photo_permission.txt`: Attribution license for the night street food market photograph

- **빠진 증빙**:
  - `확인 필요`: 원본 사진의 저작권 소유자 정보가 명시되지 않아, attribution 라이선스 적용 여부를 확정할 수 없습니다. (근거: `evidence/license/street_photo_permission.txt`는 attribution 라이선스만 제공하지만, `evidence/source/night_market_origin.txt`에서 저작권자 정보가 없음)

## 2. Purchased hand-drum rhythm

- **현재 증빙**:
  - `audio/track_final.wav`: energetic hand-drum rhythm
  - `evidence/receipt/rhythm_order.txt`: Receipt for the energetic hand-drum loop
  - `evidence/license/percussion_terms.txt`: Commercial synchronization license for the percussion recording

- **빠진 증빙**:
  - 없음

## 3. Adapted OpenPlot Mini bar chart component

- **현재 증빙**:
  - `src/lib_a.js`: bar chart component adapted from OpenPlot Mini
  - `evidence/source/chart_upstream.txt`: Upstream repository for the OpenPlot Mini bar-chart component
  - `evidence/license/chart_mit.txt`: MIT license notice for the adapted OpenPlot Mini chart component

- **빠진 증빙**:
  - 없음

## 4. Synthetic Korean weekend-market invitation voice

- **현재 증빙**:
  - `generated/voice_take.wav`: synthetic Korean narrator saying the weekend market invitation
  - `evidence/prompt/narration_prompt.txt`: 생성 프롬프트: 주말 야시장으로 초대하는 밝은 한국어 여성 내레이션

- **빠진 증빙**:
  - `확인 필요`: AI 모델 이름 및 버전이 명시되지 않아, AI 생성 기록이 완전하지 않습니다. (근거: `generated/voice_take.wav`와 `evidence/prompt/narration_prompt.txt`는 생성 프로세스를 기록하지만, 사용된 AI 모델 정보가 없음)
