# 출처·라이선스·구매증빙·AI 생성 기록 체크리스트

다음은 제출 또는 납품 전에 확인해야 할 출처, 라이선스, 구매증빙, AI 생성 기록에 대한 체크리스트입니다. 각 결과물에 사용된 입력 자산을 연결하고, 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 명시했습니다. 연결 근거가 약한 경우 `확인 필요`로 표시했습니다.

---

## 1. Custom Event Filter (src/c_02.js)

- **출처 (Source)**  
  - 현재 존재하는 증빙: `evidence/author/filter_authorship.txt` (팀이 작성한 모듈 설명)  
  - 빠진 증빙: 없음  

- **라이선스 (License)**  
  - 현재 존재하는 증빙: 없음 (팀이 직접 작성한 모듈이므로 라이선스 필요 없음)  
  - 빠진 증빙: 없음  

- **구매증빙 (Purchase proof)**  
  - 현재 존재하는 증빙: 없음 (팀이 직접 작성한 모듈이므로 구매 필요 없음)  
  - 빠진 증빙: 없음  

- **AI 생성 기록 (AI generation record)**  
  - 현재 존재하는 증빙: 없음  
  - 빠진 증빙: `확인 필요` (프로젝트가 "Synthetic dashboard build"로 명시되었으나, AI 생성 여부가 명확하지 않음)

---

## 2. ChronosLite Date Utility (src/c_01.js)

- **출처 (Source)**  
  - 현재 존재하는 증빙: `evidence/source/chronos_upstream.txt` (ChronosLite 리포지토리 URL)  
  - 빠진 증빙: 없음  

- **라이선스 (License)**  
  - 현재 존재하는 증빙: `evidence/license/chronos_license.txt` (MIT 라이선스)  
  - 빠진 증빙: 없음  

- **구매증빙 (Purchase proof)**  
  - 현재 존재하는 증빙: 없음 (MIT 라이선스로 구매 필요 없음)  
  - 빠진 증빙: 없음  

- **AI 생성 기록 (AI generation record)**  
  - 현재 존재하는 증빙: 없음  
  - 빠진 증빙: `확인 필요` (프로젝트가 "Synthetic dashboard build"로 명시되었으나, AI 생성 여부가 명확하지 않음)

---

## 3. Calendar Icon (media/i_77.svg)

- **출처 (Source)**  
  - 현재 존재하는 증빙: `evidence/source/calendar_icon_source.txt` (OpenGlyph 소스 페이지)  
  - 빠진 증빙: 없음  

- **라이선스 (License)**  
  - 현재 존재하는 증빙: `evidence/license/calendar_icon_license.txt` (CC BY 라이선스)  
  - 빠진 증빙: 없음  

- **구매증빙 (Purchase proof)**  
  - 현재 존재하는 증빙: 없음 (CC BY 라이선스로 구매 필요 없음)  
  - 빠진 증빙: 없음  

- **AI 생성 기록 (AI generation record)**  
  - 현재 존재하는 증빙: 없음  
  - 빠진 증빙: `확인 필요` (프로젝트가 "Synthetic dashboard build"로 명시되었으나, AI 생성 여부가 명확하지 않음)

---

## 4. Clock Icon (media/i_78.svg)

- **출처 (Source)**  
  - 현재 존재하는 증빙: `evidence/source/clock_icon_source.txt` (OpenGlyph 소스 페이지)  
  - 빠진 증빙: 없음  

- **라이선스 (License)**  
  - 현재 존재하는 증빙: `evidence/license/clock_icon_license.txt` (CC BY 라이선스)  
  - 빠진 증빙: 없음  

- **구매증빙 (Purchase proof)**  
  - 현재 존재하는 증빙: 없음 (CC BY 라이선스로 구매 필요 없음)  
  - 빠진 증빙: 없음  

- **AI 생성 기록 (AI generation record)**  
  - 현재 존재하는 증빙: 없음  
  - 빠진 증빙: `확인 필요` (프로젝트가 "Synthetic dashboard build"로 명시되었으나, AI 생성 여부가 명확하지 않음)

---

## 핵심 확인 사항

1. **AI 생성 기록**은 모든 결과물에 대해 `확인 필요`로 표시되었습니다.  
   - 근거: `README.md`에서 "Synthetic dashboard build"가 명시되었으나, `src/c_01.js`, `src/c_02.js`, `media/i_77.svg`, `media/i_78.svg` 등 실제 파일에서 AI 생성 여부에 대한 직접적 증거가 없습니다.  
   - 추측 금지: "Synthetic"은 프로젝트가 가상/플레이스홀더임을 의미할 수 있으나, 이는 AI 생성 여부를 확정할 수 있는 근거가 아닙니다.

2. **구매증빙**은 모든 결과물에 대해 필요하지 않습니다.  
   - 근거: ChronosLite( MIT), OpenGlyph( CC BY) 등 모든 컴포넌트가 오픈 소스 라이선스를 사용하고 있으므로 구매 증빙이 필요하지 않습니다.

3. **출처 및 라이선스**는 모든 결과물에 대해 현재 존재하는 증빙이 충분합니다.  
   - 근거: `lineage/dashboard_bundle.md`에서 명시된 컴포넌트에 대한 출처 및 라이선스 증빙이 `evidence/` 폴더에 정확히 연결되어 있습니다.

> ✅ **제출 전 필수 확인**: AI 생성 기록이 명확히 존재하는지 확인해야 합니다.  
> ❌ **추측 금지**: "Synthetic"이라는 용어만으로 AI 생성 여부를 확정하지 마세요. 실제 AI 생성 도구 사용 여부를 직접 확인해야 합니다.
