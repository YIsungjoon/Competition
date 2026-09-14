# Supabase 앨범 저장 도입 검토

- 목적: IDEA-051의 결과를 다시 열어볼 수 있는 사진 앨범으로 보존할 수 있는지 검토한다.
- 검토일: 2026-09-14
- 출처: `SRC-094`~`SRC-097`
- 상태: 기술적으로 가능, Supabase 프로젝트 연결 전 설계 제안

## 현재 구현 관찰

- 사진은 브라우저에서 긴 변 1,280px, JPEG 품질 0.76으로 다시 인코딩된다.
- 다시 인코딩한 사본은 메타데이터가 빠진 data URL로 브라우저 메모리에만 있으며 새로고침하면 사라진다.
- 현재 DB 테이블과 Supabase 클라이언트는 없다.
- 화면은 `원본 사진은 저장하지 않아요`라고 안내한다.

## 공식 문서에서 확인한 사실

- Supabase Storage의 private bucket은 다운로드에도 RLS가 적용되며, 로그인 JWT 또는 만료 시간이 있는 signed URL로 접근할 수 있다. (`SRC-094`, `SRC-095`)
- Storage 업로드 권한은 `storage.objects`의 RLS 정책으로 사용자별 폴더까지 제한할 수 있다. 서비스 키는 RLS를 우회하므로 브라우저에 노출하면 안 된다. (`SRC-094`)
- 작은 파일에는 standard upload가 적합하고, bucket 단위로 파일 크기와 MIME 유형을 제한할 수 있다. (`SRC-096`)
- 이메일 Magic Link는 비밀번호 없이 지속 계정을 만들 수 있다. 익명 로그인도 가능하지만 로그아웃·브라우저 데이터 삭제·다른 기기 사용 시 그 계정의 앨범에 다시 접근하지 못한다. (`SRC-097`)

## 제안하는 최소 흐름

1. 사진 선택·AI 대화·결과 확인까지는 지금처럼 로그인과 영구 저장 없이 진행한다.
2. 결과 화면에 `앨범으로 남기기` 버튼을 둔다.
3. 버튼을 누르면 이메일 Magic Link로 사용자를 식별하고, `원본이 아닌 최적화 사본을 삭제 전까지 저장한다`는 별도 동의를 받는다.
4. 사진은 private bucket `album-photos`의 `<user_id>/<album_id>/<photo_id>.jpg`에 저장한다.
5. Postgres에는 `albums`와 `album_photos`만 둔다. 일기 문장·질문 답변·문장별 근거·사진 시간·정렬 순서를 저장해 결과를 그대로 복원한다.
6. 앨범 화면은 짧은 만료 시간의 signed URL로 사진을 표시한다.
7. `앨범 삭제`는 Storage 객체와 DB 행을 모두 제거하고, 일부만 실패하면 재시도 가능한 오류로 남긴다.

## 최소 데이터 구조

### `albums`

- `id uuid primary key`
- `user_id uuid not null`
- `title text not null`
- `reflection jsonb not null`: 질문·답변·일기 문장·근거
- `occurred_on date null`
- `created_at timestamptz not null`

### `album_photos`

- `id uuid primary key`
- `album_id uuid not null`
- `storage_path text not null`
- `taken_at timestamptz null`: 현재는 원본 EXIF가 아니라 파일 수정 시각
- `sort_order integer not null`

두 테이블 모두 `auth.uid() = user_id` 또는 소유 앨범 조인 조건으로 SELECT·INSERT·DELETE를 제한한다. 브라우저에는 publishable key만 두고 service-role key는 두지 않는다.

## 해석과 결정 영향

- INTERPRETATION: 앨범 저장은 결과를 일회성 AI 생성물에서 다시 돌아보는 개인 기록으로 바꾸므로 IDEA-051의 저장 가치를 강화한다.
- INTERPRETATION: 반대로 자동 저장은 현재의 개인정보 약속을 깨고 핵심 AI 경험과 무관한 계정·동기화 범위를 앞당긴다.
- PROPOSAL: 핵심 흐름은 무저장으로 유지하고, 결과를 본 사용자가 명시적으로 선택할 때만 최적화 사본과 기록을 private 저장한다.

## 제외 범위와 한계

- 이번 단계에서는 공개 공유 링크, 공동 앨범, 댓글, 원본 사진 보관, 자동 백업을 제외한다.
- Supabase 프로젝트 URL과 publishable key가 없어 실제 bucket·RLS·업로드는 아직 검증하지 않았다.
- 익명 로그인은 심사 시 체험 마찰은 적지만 지속 앨범이라는 약속과 맞지 않아 기본안에서 제외했다. 필요하면 `저장 없는 체험`에만 사용할 수 있다.
- 사진은 민감정보일 수 있으므로 보관 기간·계정 삭제·앨범 삭제 문구를 실제 배포 전에 다시 검토해야 한다.

## 다음 작업

1. Supabase 프로젝트와 publishable key를 준비한다.
2. private bucket, 두 테이블, RLS를 생성한다.
3. 결과 화면의 `앨범으로 남기기`와 `내 앨범` 한 화면만 구현한다.
4. 다른 사용자로 접근 차단, URL 만료, 앨범 완전 삭제를 검증한다.
