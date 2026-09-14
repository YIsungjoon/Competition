아래에는 한 프로젝트 폴더의 파일 경로와 각 파일에서 읽을 수 있는 내용이 제공됩니다. 이 자료만 사용해 제출 또는 납품 전에 사람이 확인해야 할 출처·라이선스·구매증빙·AI 생성 기록 체크리스트를 작성하세요.

각 결과물에 사용된 것으로 보이는 입력 자산을 연결하고, 각 입력 자산에 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 나누어 적으세요. 연결 근거가 약하면 추측으로 확정하지 말고 `확인 필요`라고 표시하세요. `권리가 있다`, `침해다`, `법적으로 사용 가능하다` 같은 법률 결론은 내리지 마세요.

형식은 사람이 읽는 Markdown 체크리스트로 자유롭게 작성하되, 판단마다 근거가 된 파일 경로를 적으세요.

## 프로젝트 입력

### FILE: README.md
```text
Files were renamed during export. Descriptions remain in project notes.
```

### FILE: audio/track_final.wav
```text
SYNTHETIC PLACEHOLDER
energetic hand-drum rhythm purchased for a short social reel
```

### FILE: deliverables/reel_v7.mp4
```text
SYNTHETIC PLACEHOLDER
vertical weekend-market reel with night street, drums, chart and Korean narration
```

### FILE: evidence/license/chart_mit.txt
```text
MIT license notice for the adapted OpenPlot Mini chart component
```

### FILE: evidence/license/percussion_terms.txt
```text
Commercial synchronization license for the upbeat percussion recording
```

### FILE: evidence/license/street_photo_permission.txt
```text
Attribution license for the night street food market photograph
```

### FILE: evidence/prompt/narration_prompt.txt
```text
생성 프롬프트: 주말 야시장으로 초대하는 밝은 한국어 여성 내레이션
```

### FILE: evidence/receipt/rhythm_order.txt
```text
Receipt for the energetic hand-drum loop used in the weekend reel
```

### FILE: evidence/source/chart_upstream.txt
```text
Upstream repository for the OpenPlot Mini bar-chart component
```

### FILE: evidence/source/night_market_origin.txt
```text
원본 주소: 네온 간판이 빛나는 야시장 골목의 거리 사진
```

### FILE: generated/voice_take.wav
```text
SYNTHETIC PLACEHOLDER
synthetic Korean narrator saying the weekend market invitation
```

### FILE: lineage/reel_notes.md
```text
Output: deliverables/reel_v7.mp4
Ingredient: a neon-lit evening food market scene photographed at street level
Ingredient: an energetic purchased hand-drum rhythm
Ingredient: the adapted OpenPlot Mini bar chart component
Ingredient: a synthetic Korean weekend-market invitation voice
```

### FILE: media/img_1042.png
```text
SYNTHETIC PLACEHOLDER
neon-lit evening food market photographed at street level
```

### FILE: notes/edit_log.md
```text
The editor normalized media filenames before final render.
```

### FILE: src/lib_a.js
```text
SYNTHETIC PLACEHOLDER
bar chart component adapted from the OpenPlot Mini library
```

## 공통 자산 선언

다음 선언은 비교하는 두 조건에 동일하게 제공됩니다. 관계·누락 정답은 포함하지 않습니다.

```json
{
  "subjects": [
    {
      "path": "media/img_1042.png",
      "description": "neon-lit evening food market photographed at street level",
      "origin_type": "third_party_free"
    },
    {
      "path": "audio/track_final.wav",
      "description": "energetic hand-drum rhythm purchased for a short social reel",
      "origin_type": "purchased"
    },
    {
      "path": "src/lib_a.js",
      "description": "bar chart component adapted from the OpenPlot Mini library",
      "origin_type": "open_source"
    },
    {
      "path": "generated/voice_take.wav",
      "description": "synthetic Korean narrator saying the weekend market invitation",
      "origin_type": "ai_generated"
    },
    {
      "path": "deliverables/reel_v7.mp4",
      "description": "vertical weekend-market reel with night street, drums, chart and Korean narration",
      "origin_type": "output"
    }
  ]
}
```