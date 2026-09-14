# RightsLedger MVP

프로젝트 폴더를 브라우저에서 불러오면 로컬 `bge-m3`가 이름이 바뀐 자산과 증거의 의미 관계를 제안한다. 사용자가 AI 제안을 확인·수정·제외한 뒤 누락 증거, SHA-256 인벤토리, 분리된 C2PA 상태를 JSON 감사 기록으로 내려받는다.

## 실행

요구 환경은 Python 표준 라이브러리, Ollama의 `bge-m3:latest`, 선택 사항인 `c2patool`이다. 외부 Python·JavaScript 패키지는 없다.

```bash
ollama serve
python3 05_deliverables/rightsledger_mvp/app.py --port 8765
```

브라우저에서 `http://127.0.0.1:8765`를 연다. 개발용 입력으로는 `06_experiments/rightsledger_24h/cases/CASE-002/project`를 선택할 수 있다. 이 사례는 이미 개발 확인에 사용했으므로 정식 1인 형성평가에는 재사용하지 않는다.

## 입력 계약

선택한 폴더 최상위에 `.rightsledger_observations.json`이 필요하다.

```json
{
  "subjects": [
    {
      "path": "media/hero.png",
      "description": "wide blue skyline used as the hero image",
      "origin_type": "third_party_free"
    }
  ]
}
```

`origin_type`은 `third_party_free`, `purchased`, `open_source`, `ai_generated`, `original`, `output` 중 하나다. 증거 파일은 `evidence/<종류>/`, 결과물 구성 기록은 `lineage/*.md`에 둔다. 현재 입력 크기 제한은 파일 200개, 파일당 5MB, 전체 25MB다.

## 데이터·판단 경계

- 브라우저가 보낸 파일은 요청 메모리와 C2PA 임시 폴더에서만 처리하며 서버에 저장하지 않는다.
- 정확 경로 연결과 SHA-256·필수 증거 계산은 결정론적이다.
- 이름이 바뀐 단서만 로컬 `bge-m3` 임베딩으로 비교한다. AI 제안은 사용자가 확인하기 전까지 `검토 필요`다.
- C2PA의 매니페스트 존재, 무결성, 서명자 신뢰, 권리 허락 상태를 분리한다.
- 법률상 권리 보유·침해·제출 가능 결론은 생성하지 않는다.
- 실제 이미지·음원 내용 설명은 아직 구현하지 않았으며 `.rightsledger_observations.json`을 사용자/VLM 입력 경계로 둔다.

## 검사

```bash
python3 05_deliverables/rightsledger_mvp/app.py --self-check
```

이 검사는 정확 관계 연결, 필수 증거 재계산, 경로 탈출 차단을 확인한다. 실제 AI·브라우저·C2PA 종단간 결과는 FDS 작업 로그에 별도로 기록한다.
