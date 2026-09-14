아래에는 한 프로젝트 폴더의 파일 경로와 각 파일에서 읽을 수 있는 내용이 제공됩니다. 이 자료만 사용해 제출 또는 납품 전에 사람이 확인해야 할 출처·라이선스·구매증빙·AI 생성 기록 체크리스트를 작성하세요.

각 결과물에 사용된 것으로 보이는 입력 자산을 연결하고, 각 입력 자산에 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 나누어 적으세요. 연결 근거가 약하면 추측으로 확정하지 말고 `확인 필요`라고 표시하세요. `권리가 있다`, `침해다`, `법적으로 사용 가능하다` 같은 법률 결론은 내리지 마세요.

형식은 사람이 읽는 Markdown 체크리스트로 자유롭게 작성하되, 판단마다 근거가 된 파일 경로를 적으세요.

## 프로젝트 입력

### FILE: README.md
```text
Synthetic control project with explicit file references.
```

### FILE: audio/calm_piano.wav
```text
SYNTHETIC PLACEHOLDER
calm piano instrumental bed for the launch video
```

### FILE: deliverables/launch_video.mp4
```text
SYNTHETIC PLACEHOLDER
launch video combining the skyline, piano bed and tagline
```

### FILE: evidence/license/hero_license.txt
```text
License for media/hero_skyline.png: CC BY 4.0
```

### FILE: evidence/license/piano_license.txt
```text
Commercial media license for audio/calm_piano.wav
```

### FILE: evidence/license/player_license.txt
```text
SPDX-License-Identifier: MIT
Applies to src/player.js
```

### FILE: evidence/model_terms/tagline_terms.txt
```text
Model terms snapshot for generated/tagline.png, tool: SyntheticCanvas
```

### FILE: evidence/prompt/tagline_prompt.txt
```text
Prompt record for generated/tagline.png: warm Korean launch phrase
```

### FILE: evidence/receipt/piano_receipt.txt
```text
Purchase receipt for audio/calm_piano.wav, order SYN-1001
```

### FILE: evidence/source/hero_source.txt
```text
Source for media/hero_skyline.png: https://example.test/skyline
```

### FILE: evidence/source/player_source.txt
```text
Upstream source for src/player.js: https://example.test/wavekit
```

### FILE: generated/tagline.png
```text
SYNTHETIC PLACEHOLDER
AI-generated Korean campaign tagline on a transparent background
```

### FILE: lineage/launch_video.md
```text
Output: deliverables/launch_video.mp4
Ingredient: media/hero_skyline.png
Ingredient: audio/calm_piano.wav
Ingredient: generated/tagline.png
```

### FILE: media/hero_skyline.png
```text
SYNTHETIC PLACEHOLDER
wide blue night city skyline used as a hero background
```

### FILE: src/player.js
```text
SYNTHETIC PLACEHOLDER
JavaScript audio player adapted from the WaveKit project
```

## 공통 자산 선언

다음 선언은 비교하는 두 조건에 동일하게 제공됩니다. 관계·누락 정답은 포함하지 않습니다.

```json
{
  "subjects": [
    {
      "path": "media/hero_skyline.png",
      "description": "wide blue night city skyline used as a hero background",
      "origin_type": "third_party_free"
    },
    {
      "path": "audio/calm_piano.wav",
      "description": "calm piano instrumental bed for the launch video",
      "origin_type": "purchased"
    },
    {
      "path": "src/player.js",
      "description": "JavaScript audio player adapted from the WaveKit project",
      "origin_type": "open_source"
    },
    {
      "path": "generated/tagline.png",
      "description": "AI-generated Korean campaign tagline on a transparent background",
      "origin_type": "ai_generated"
    },
    {
      "path": "deliverables/launch_video.mp4",
      "description": "launch video combining the skyline, piano bed and tagline",
      "origin_type": "output"
    }
  ]
}
```