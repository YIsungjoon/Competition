아래에는 한 프로젝트 폴더의 파일 경로와 각 파일에서 읽을 수 있는 내용이 제공됩니다. 이 자료만 사용해 제출 또는 납품 전에 사람이 확인해야 할 출처·라이선스·구매증빙·AI 생성 기록 체크리스트를 작성하세요.

각 결과물에 사용된 것으로 보이는 입력 자산을 연결하고, 각 입력 자산에 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 나누어 적으세요. 연결 근거가 약하면 추측으로 확정하지 말고 `확인 필요`라고 표시하세요. `권리가 있다`, `침해다`, `법적으로 사용 가능하다` 같은 법률 결론은 내리지 마세요.

형식은 사람이 읽는 Markdown 체크리스트로 자유롭게 작성하되, 판단마다 근거가 된 파일 경로를 적으세요.

## 프로젝트 입력

### FILE: README.md
```text
Synthetic dashboard build.
```

### FILE: deliverables/dashboard.zip
```text
SYNTHETIC PLACEHOLDER
dashboard bundle containing date helper, custom filter and two outline icons
```

### FILE: evidence/author/filter_authorship.txt
```text
Team declaration for the custom event filtering module
```

### FILE: evidence/license/calendar_icon_license.txt
```text
CC BY license for the OpenGlyph outline calendar symbol
```

### FILE: evidence/license/chronos_license.txt
```text
MIT license notice for the ChronosLite date utility
```

### FILE: evidence/license/clock_icon_license.txt
```text
CC BY license for the OpenGlyph outline clock symbol
```

### FILE: evidence/source/calendar_icon_source.txt
```text
Source page for the outline calendar symbol in OpenGlyph
```

### FILE: evidence/source/chronos_upstream.txt
```text
Repository URL for the ChronosLite date-formatting helper
```

### FILE: evidence/source/clock_icon_source.txt
```text
Source page for the outline clock symbol in OpenGlyph
```

### FILE: lineage/dashboard_bundle.md
```text
Output: deliverables/dashboard.zip
Ingredient: the ChronosLite date-formatting helper
Ingredient: the team's custom event filter
Ingredient: the outline calendar symbol from OpenGlyph
Ingredient: the outline clock symbol from OpenGlyph
```

### FILE: media/i_77.svg
```text
SYNTHETIC PLACEHOLDER
outline calendar icon from the OpenGlyph collection
```

### FILE: media/i_78.svg
```text
SYNTHETIC PLACEHOLDER
outline clock icon from the OpenGlyph collection
```

### FILE: package.json
```text
{"name":"synthetic-dashboard","private":true}
```

### FILE: src/c_01.js
```text
SYNTHETIC PLACEHOLDER
date formatting helper adapted from the ChronosLite package
```

### FILE: src/c_02.js
```text
SYNTHETIC PLACEHOLDER
custom event filter written entirely by the project team
```

## 공통 자산 선언

다음 선언은 비교하는 두 조건에 동일하게 제공됩니다. 관계·누락 정답은 포함하지 않습니다.

```json
{
  "subjects": [
    {
      "path": "src/c_01.js",
      "description": "date formatting helper adapted from the ChronosLite package",
      "origin_type": "open_source"
    },
    {
      "path": "src/c_02.js",
      "description": "custom event filter written entirely by the project team",
      "origin_type": "original"
    },
    {
      "path": "media/i_77.svg",
      "description": "outline calendar icon from the OpenGlyph collection",
      "origin_type": "third_party_free"
    },
    {
      "path": "media/i_78.svg",
      "description": "outline clock icon from the OpenGlyph collection",
      "origin_type": "third_party_free"
    },
    {
      "path": "deliverables/dashboard.zip",
      "description": "dashboard bundle containing date helper, custom filter and two outline icons",
      "origin_type": "output"
    }
  ]
}
```