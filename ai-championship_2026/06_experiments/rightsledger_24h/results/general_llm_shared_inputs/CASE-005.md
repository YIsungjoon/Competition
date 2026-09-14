아래에는 한 프로젝트 폴더의 파일 경로와 각 파일에서 읽을 수 있는 내용이 제공됩니다. 이 자료만 사용해 제출 또는 납품 전에 사람이 확인해야 할 출처·라이선스·구매증빙·AI 생성 기록 체크리스트를 작성하세요.

각 결과물에 사용된 것으로 보이는 입력 자산을 연결하고, 각 입력 자산에 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 나누어 적으세요. 연결 근거가 약하면 추측으로 확정하지 말고 `확인 필요`라고 표시하세요. `권리가 있다`, `침해다`, `법적으로 사용 가능하다` 같은 법률 결론은 내리지 마세요.

형식은 사람이 읽는 Markdown 체크리스트로 자유롭게 작성하되, 판단마다 근거가 된 파일 경로를 적으세요.

## 프로젝트 입력

### FILE: README.md
```text
Synthetic product landing page.
```

### FILE: deliverables/landing_page.zip
```text
SYNTHETIC PLACEHOLDER
landing page with amber bottle, ocean background, rounded headline and custom CSS
```

### FILE: evidence/author/css_authorship.txt
```text
Team authorship statement for the custom landing-page layout stylesheet
```

### FILE: evidence/license/rounded_type_license.txt
```text
Open font license for the rounded display typeface used in the headline
```

### FILE: evidence/model_terms/amber_terms.txt
```text
Terms snapshot for the image model used for the amber bottle render
```

### FILE: evidence/model_terms/ocean_terms.txt
```text
Terms snapshot for the image model used for the blue ocean texture
```

### FILE: evidence/prompt/amber_prompt.txt
```text
Prompt record: photoreal amber glass bottle centered on a clean white studio background
```

### FILE: evidence/prompt/ocean_prompt.txt
```text
Prompt record: abstract blue ocean-water texture seen from above
```

### FILE: evidence/source/unrelated_drone_source.txt
```text
Source URL for mountain drone footage used in an abandoned travel-film draft
```

### FILE: generated/g_amber.png
```text
SYNTHETIC PLACEHOLDER
AI-generated amber glass bottle product render on white
```

### FILE: generated/g_ocean.png
```text
SYNTHETIC PLACEHOLDER
AI-generated blue ocean texture used as a background
```

### FILE: lineage/landing_bundle.md
```text
Output: deliverables/landing_page.zip
Ingredient: the AI-created amber glass bottle product render
Ingredient: the AI-created blue ocean background texture
Ingredient: the rounded display headline typeface
Ingredient: the team's custom landing-page layout styles
```

### FILE: media/font_z.woff
```text
SYNTHETIC PLACEHOLDER
rounded display typeface used for the product headline
```

### FILE: notes/provenance_notes.md
```text
One source record belongs to an abandoned draft and must not be auto-attached.
```

### FILE: src/landing.css
```text
SYNTHETIC PLACEHOLDER
landing-page layout styles written by the project team
```

## 공통 자산 선언

다음 선언은 비교하는 두 조건에 동일하게 제공됩니다. 관계·누락 정답은 포함하지 않습니다.

```json
{
  "subjects": [
    {
      "path": "generated/g_amber.png",
      "description": "AI-generated amber glass bottle product render on white",
      "origin_type": "ai_generated"
    },
    {
      "path": "generated/g_ocean.png",
      "description": "AI-generated blue ocean texture used as a background",
      "origin_type": "ai_generated"
    },
    {
      "path": "media/font_z.woff",
      "description": "rounded display typeface used for the product headline",
      "origin_type": "third_party_free"
    },
    {
      "path": "src/landing.css",
      "description": "landing-page layout styles written by the project team",
      "origin_type": "original"
    },
    {
      "path": "deliverables/landing_page.zip",
      "description": "landing page with amber bottle, ocean background, rounded headline and custom CSS",
      "origin_type": "output"
    }
  ]
}
```