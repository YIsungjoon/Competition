아래에는 한 프로젝트 폴더의 파일 경로와 각 파일에서 읽을 수 있는 내용이 제공됩니다. 이 자료만 사용해 제출 또는 납품 전에 사람이 확인해야 할 출처·라이선스·구매증빙·AI 생성 기록 체크리스트를 작성하세요.

각 결과물에 사용된 것으로 보이는 입력 자산을 연결하고, 각 입력 자산에 현재 존재하는 증빙과 빠진 것으로 보이는 증빙을 나누어 적으세요. 연결 근거가 약하면 추측으로 확정하지 말고 `확인 필요`라고 표시하세요. `권리가 있다`, `침해다`, `법적으로 사용 가능하다` 같은 법률 결론은 내리지 마세요.

형식은 사람이 읽는 Markdown 체크리스트로 자유롭게 작성하되, 판단마다 근거가 된 파일 경로를 적으세요.

## 프로젝트 입력

### FILE: README.md
```text
Two similar guitar takes remain in the folder.
```

### FILE: deliverables/podcast_ep1.wav
```text
SYNTHETIC PLACEHOLDER
first podcast episode with acoustic intro and electronic logo sting
```

### FILE: evidence/author/portrait_author.txt
```text
Team authorship statement for the founder portrait shot in window light
```

### FILE: evidence/license/guitar_standard_license.txt
```text
Podcast synchronization license for the selected standard-tempo gentle guitar take
```

### FILE: evidence/model_terms/sting_model_terms.txt
```text
Terms snapshot for the audio model used to create the electronic three-note logo sting
```

### FILE: evidence/prompt/sting_prompt.txt
```text
Prompt: a concise electronic three-note sonic logo for a podcast
```

### FILE: evidence/receipt/guitar_standard_order.txt
```text
Order receipt for the standard-tempo acoustic guitar intro recording
```

### FILE: exports/cover_preview.txt
```text
Placeholder for a non-audited preview export.
```

### FILE: generated/music_sting.wav
```text
SYNTHETIC PLACEHOLDER
short electronic three-note logo sting generated for the show
```

### FILE: lineage/episode_cue.md
```text
Output: deliverables/podcast_ep1.wav
Ingredient: the selected standard-tempo gentle acoustic guitar intro
Ingredient: the generated electronic three-note show logo
```

### FILE: media/a_17.wav
```text
SYNTHETIC PLACEHOLDER
standard-tempo gentle acoustic guitar recording selected for the podcast intro
```

### FILE: media/a_18.wav
```text
SYNTHETIC PLACEHOLDER
slower alternate gentle acoustic guitar recording not selected for the intro
```

### FILE: media/photo_x.png
```text
SYNTHETIC PLACEHOLDER
founder portrait photographed beside a window in soft daylight
```

### FILE: notes/guest_topics.md
```text
Synthetic interview topic list.
```

### FILE: notes/mix_settings.txt
```text
Intro -12 LUFS; speech -16 LUFS.
```

## 공통 자산 선언

다음 선언은 비교하는 두 조건에 동일하게 제공됩니다. 관계·누락 정답은 포함하지 않습니다.

```json
{
  "subjects": [
    {
      "path": "media/a_17.wav",
      "description": "standard-tempo gentle acoustic guitar recording selected for the podcast intro",
      "origin_type": "purchased"
    },
    {
      "path": "media/a_18.wav",
      "description": "slower alternate gentle acoustic guitar recording not selected for the intro",
      "origin_type": "purchased"
    },
    {
      "path": "media/photo_x.png",
      "description": "founder portrait photographed beside a window in soft daylight",
      "origin_type": "original"
    },
    {
      "path": "generated/music_sting.wav",
      "description": "short electronic three-note logo sting generated for the show",
      "origin_type": "ai_generated"
    },
    {
      "path": "deliverables/podcast_ep1.wav",
      "description": "first podcast episode with acoustic intro and electronic logo sting",
      "origin_type": "output"
    }
  ]
}
```