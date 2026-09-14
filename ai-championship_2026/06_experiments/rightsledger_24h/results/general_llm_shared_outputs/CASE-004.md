# 출처·라이선스·구매증빙·AI 생성 기록 체크리스트

다음은 프로젝트가 제출 전에 확인해야 할 **입력 자산별 증빙 상태**를 기술한 체크리스트입니다. 각 입력 자산에 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 기술하며, 연결 근거가 약한 경우 `확인 필요`로 표시합니다.

---

## 1. Custom Event Filter (src/c_02.js)

- **현재 존재하는 증빙**:
  - `lineage/dashboard_bundle.md`: "Ingredient: the team's custom event filter" → 프로젝트 팀이 완전히 작성한 것으로 명시됨.
  - `src/c_02.js`: "SYNTHETIC PLACEHOLDER" 텍스트로 팀이 직접 작성한 커스텀 필터임을 나타냄.

- **빠진 것으로 보이는 증빙**:
  - **라이선스**: 프로젝트 팀의 커스텀 코드에 대한 라이선스 정의가 누락됨. `package.json`에 라이선스 필드가 없으며, 해당 컴포넌트에 대한 별도 라이선스 파일이 존재하지 않음. `확인 필요`
  - **AI 생성 기록**: `src/c_02.js`의 "SYNTHETIC PLACEHOLDER"는 AI 생성을 암시하지만, 팀이 직접 작성했다고 명시됨. AI 도구 사용 여부 확인 필요. `확인 필요`

---

## 2. ChronosLite Date Utility (src/c_01.js)

- **현재 존재하는 증빙**:
  - `evidence/license/chronos_license.txt`: MIT 라이선스 정책 명시.
  - `evidence/source/chronos_upstream.txt`: ChronosLite의 리포지토리 URL 제공.
  - `src/c_01.js`: "SYNTHETIC PLACEHOLDER" 텍스트로 ChronosLite에서 적응한 코드임을 나타냄.

- **빠진 것으로 보이는 증빙**:
  - **적응 문서**: ChronosLite 코드를 적응한 과정에 대한 문서화(예: 변경 로그, 버전 정보)가 누락됨. `확인 필요`

---

## 3. Calendar Icon (media/i_77.svg)

- **현재 존재하는 증빙**:
  - `evidence/license/calendar_icon_license.txt`: OpenGlyph의 CC BY 라이선스 정책 명시.
  - `evidence/source/calendar_icon_source.txt`: OpenGlyph에서의 캘린더 아이콘 소스 페이지 링크.
  - `media/i_77.svg`: OpenGlyph 컬렉션에서의 캘린더 아이콘.

- **빠진 것으로 보이는 증빙**:
  - 없음.

---

## 4. Clock Icon (media/i_78.svg)

- **현재 존재하는 증빙**:
  - `evidence/license/clock_icon_license.txt`: OpenGlyph의 CC BY 라이선스 정책 명시.
  - `evidence/source/clock_icon_source.txt`: OpenGlyph에서의 클록 아이콘 소스 페이지 링크.
  - `media/i_78.svg`: OpenGlyph 컬렉션에서의 클록 아이콘.

- **빠진 것으로 보이는 증빙**:
  - 없음.

---

## 5. 구매증빙 확인 (추가 사항)

- **현재 존재하는 증빙**:
  - 모든 third-party 자산(OpenGlyph 아이콘, ChronosLite)은 **무료 라이선스**로 제공되므로 구매증빙이 필요하지 않음.

- **빠진 것으로 보이는 증빙**:
  - 없음.

---

> 💡 **주의**:  
> - `구매증빙`은 모든 third-party 자산이 **CC BY** 또는 **MIT** 등 무료 라이선스로 제공되므로 **필요하지 않음**.
> - `AI 생성 기록`은 `src/c_02.js`와 `src/c_01.js`에서 "SYNTHETIC PLACEHOLDER" 텍스트로 인해 추측 가능하지만, 실제 AI 도구 사용 여부는 **확인 필요**.
> - 모든 입력 자산에 대한 **라이선스**와 **출처**는 `evidence/` 디렉토리에서 명확히 확인 가능하지만, **적응 문서** 및 **AI 사용 기록**은 추가 확인이 필요합니다.