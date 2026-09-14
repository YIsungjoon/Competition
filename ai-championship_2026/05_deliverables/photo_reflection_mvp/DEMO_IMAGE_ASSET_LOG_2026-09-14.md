# IDEA-051 프런트 예시 사진 제작 기록

- 제작일: 2026-09-14
- 제작 도구: Codex 내장 `image_gen`
- 용도: 개인정보를 올리지 않고도 결과 화면과 문장 근거 탐색을 확인하는 프런트 내장 예시
- 상태: 합성 이미지이며 실제 사용자의 하루나 실제 AI 분석 결과가 아님

## 공통 제작 조건

- 유형: `photorealistic-natural`
- 형식: 가로 4:3의 자연스러운 스마트폰 생활 사진
- 연결성: 조용한 토요일의 아침 카페 → 오후 산책 → 산책 중 벤치 → 저녁 책상
- 안전·표현 조건: 식별 가능한 인물, 얼굴, 상표, 워터마크, 읽을 수 있는 문구, 콜라주를 넣지 않는다.
- 이유: 기존 고정 샘플의 시간·관찰·질문·일기 근거를 바꾸지 않고, 추상 SVG만 실제 사진과 가까운 시각 단서로 교체하기 위해서다.

## 최종 프롬프트 세트

### P01 — 아침 카페

> A candid first-person lifestyle photo from a quiet Saturday morning at a small contemporary neighborhood cafe, showing a ceramic drink cup and an open book on a wooden table beside a window. Realistic smartphone photography with natural imperfections, landscape 4:3, eye-level seated viewpoint, gentle warm morning light, warm cream and natural wood. No identifiable person, logos, readable text, watermark, or collage.

### P02 — 오후 산책로

> A candid first-person lifestyle photo from a quiet Saturday afternoon walk on a tree-lined path in an ordinary neighborhood park in Korea, with long leaf shadows and the path continuing ahead. Realistic smartphone photography with natural imperfections, landscape 4:3, walking eye-level viewpoint, soft afternoon sunlight, muted green and warm gray. No identifiable person, logos, readable text, watermark, or collage.

### P03 — 산책 중 벤치

> A candid first-person detail photo during the same quiet Saturday walk, showing sunlight moving through leaves and a small weathered bench at the edge of the path in the same ordinary Korean neighborhood park. Realistic smartphone photography, landscape 4:3, closer observational handheld frame, deep green and warm sunlit brown. No identifiable person, logos, readable text, watermark, or collage.

### P04 — 저녁 책상

> A candid first-person lifestyle photo from the evening of the same quiet Saturday, showing a small desk lamp turned on, a blank cream notepad, and a pen on a modest lived-in apartment desk. Realistic smartphone photography, landscape 4:3, seated viewpoint, warm lamplight with cool dusk shadows, charcoal, amber, and cream. No readable writing, identifiable person, logos, text, watermark, or collage.

## 프로젝트 반입 결과

내장 도구의 PNG 결과를 프로젝트에 복사한 뒤 긴 변 1,280px, JPEG 품질 76으로 변환했다.

| 화면 순서 | 프로젝트 파일 | 크기 | SHA-256 |
|---:|---|---:|---|
| P01 | `site/public/demo/saturday-01-cafe.jpg` | 1280×960 | `e064bac11ad69701507480ff2f9f0593e8368a8d23604230be29f509cc827615` |
| P02 | `site/public/demo/saturday-02-walk.jpg` | 1280×960 | `e60a83efc047e23c888b55414a61d42eec5ddc49229e23022558030995a4846d` |
| P03 | `site/public/demo/saturday-03-bench.jpg` | 1280×960 | `52283167fb54a8f9ac0d3f5a13f9d4fb5912fa8d1b0f0c7cfc3801cad964de2d` |
| P04 | `site/public/demo/saturday-04-desk.jpg` | 1280×960 | `dccb34604a7116f47b325e285b3d4d994238d0e7a847c6b8b964eb321984a34b` |

## 직접 관찰과 한계

- 네 장 모두 얼굴·인물·상표·워터마크 없이 기존 샘플의 네 시점과 대응한다.
- P01의 펼친 책에는 문장처럼 보이는 질감이 있으나 화면에서 읽을 수 있는 실제 문구는 식별되지 않는다.
- 사진과 결과는 서로 맞도록 사람이 미리 작성한 고정 예시다. 실제 모델이 이 네 장을 분석해 같은 질문과 일기를 만들었다는 증거로 사용하면 안 된다.
- 화면 안내에 `AI로 제작한 예시 사진과 고정된 예시 결과`라고 표시한다.
