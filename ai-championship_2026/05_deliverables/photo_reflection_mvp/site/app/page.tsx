"use client";
/* eslint-disable @next/next/no-img-element */

import { useEffect, useRef, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Check,
  Clock3,
  Copy,
  Download,
  Eye,
  ImagePlus,
  Images,
  LoaderCircle,
  LockKeyhole,
  MessageCircle,
  RotateCcw,
  Sparkles,
  X,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";
import type {
  DiaryResult,
  ReflectionAnalysis,
  ReflectionAnswer,
} from "@/lib/reflection";

type Stage = "upload" | "interview" | "result";

type LocalPhoto = {
  clientId: string;
  name: string;
  time: number;
  dataUrl: string;
};

const MAX_PHOTOS = 8;

const demoAnalysis: ReflectionAnalysis = {
  timelineTitle: "조금 천천히 흘러간 토요일",
  moments: [
    { id: "M01", label: "오전 9:12", observation: "창가 테이블에 음료와 펼친 책이 보인다.", unknown: "이 시간을 사진으로 남긴 이유는 보이지 않는다.", photoIds: ["P01"] },
    { id: "M02", label: "오후 2:36", observation: "나무 그림자가 드리운 산책로가 이어진다.", unknown: "어디로 향했는지, 누구와 걸었는지는 알 수 없다.", photoIds: ["P02", "P03"] },
    { id: "M03", label: "저녁 7:48", observation: "메모가 놓인 책상 위로 작은 조명이 켜져 있다.", unknown: "메모를 쓰게 된 계기는 사진 밖에 있다.", photoIds: ["P04"] },
  ],
  questions: [
    { id: "Q01", text: "카페를 나와 산책로로 향하는 사이, 사진에는 남지 않았지만 오늘의 흐름을 바꾼 일이 있었나요?", intent: "사진 사이의 변화", photoIds: ["P01", "P02"] },
    { id: "Q02", text: "산책하면서 유난히 오래 듣거나 생각했던 말, 소리, 혹은 이유가 있었나요?", intent: "사진 밖의 감각과 이유", photoIds: ["P02", "P03"] },
    { id: "Q03", text: "오늘을 나중에 다시 펼쳤을 때 가장 먼저 기억하고 싶은 한 문장은 무엇인가요?", intent: "남기고 싶은 의미", photoIds: ["P04"] },
  ],
};

const demoAnswers = [
  "약속이 취소됐지만 바로 집에 가지 않고, 오랜만에 아무 목적 없이 걸어보기로 했다.",
  "바람에 나뭇잎 부딪히는 소리가 생각보다 크게 들렸다. 서두르지 않아도 된다는 느낌이 좋았다.",
  "계획이 비어도 하루까지 비는 것은 아니다.",
];

const demoDiary: DiaryResult = {
  title: "계획이 비어도 하루는 남는다",
  sentences: [
    { id: "S01", text: "토요일 아침, 창가에서 책을 펼쳐 둔 채 한동안 머물렀다.", sources: ["P01"] },
    { id: "S02", text: "약속이 취소됐지만 바로 집에 가지 않고, 아무 목적 없이 걸어보기로 했다.", sources: ["U01", "P02"] },
    { id: "S03", text: "산책로에서는 바람에 나뭇잎이 부딪히는 소리가 생각보다 크게 들렸다.", sources: ["U02", "P02", "P03"] },
    { id: "S04", text: "서두르지 않아도 된다는 느낌을 오래 붙잡고 싶어 저녁 책상에 메모를 남겼다.", sources: ["U02", "P04"] },
    { id: "S05", text: "계획이 비어도 하루까지 비는 것은 아니다.", sources: ["U03"] },
  ],
};

const demoPhotos: LocalPhoto[] = [
  ["09:12", "saturday-01-cafe.jpg"],
  ["14:36", "saturday-02-walk.jpg"],
  ["15:08", "saturday-03-bench.jpg"],
  ["19:48", "saturday-04-desk.jpg"],
].map(([label, filename], index) => ({
  clientId: `demo-${index}`,
  name: filename,
  time: new Date(`2026-09-12T${label}:00+09:00`).getTime(),
  dataUrl: `/demo/${filename}`,
}));

function photoId(index: number) {
  return `P${String(index + 1).padStart(2, "0")}`;
}

async function removeMetadata(file: File): Promise<LocalPhoto> {
  const bitmap = await createImageBitmap(file);
  const ratio = Math.min(1, 1280 / Math.max(bitmap.width, bitmap.height));
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(bitmap.width * ratio);
  canvas.height = Math.round(bitmap.height * ratio);
  const context = canvas.getContext("2d");

  if (!context) throw new Error("사진을 읽을 수 없습니다.");
  context.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
  bitmap.close();

  return {
    clientId: crypto.randomUUID(),
    name: file.name,
    time: file.lastModified,
    dataUrl: canvas.toDataURL("image/jpeg", 0.76),
  };
}

async function postReflection(body: Record<string, unknown>) {
  const response = await fetch("/api/reflect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const value = await response.json().catch(() => null);
  if (!response.ok) {
    const message = value?.error?.message || "AI 작업을 완료하지 못했습니다.";
    const error = new Error(message) as Error & { code?: string };
    error.code = value?.error?.code;
    throw error;
  }
  return value;
}

export default function Home() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [stage, setStage] = useState<Stage>("upload");
  const [photos, setPhotos] = useState<LocalPhoto[]>([]);
  const [analysis, setAnalysis] = useState<ReflectionAnalysis | null>(null);
  const [answers, setAnswers] = useState(["", "", ""]);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [diary, setDiary] = useState<DiaryResult | null>(null);
  const [sourceFocus, setSourceFocus] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState<"prepare" | "analyze" | "compose" | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isDemo, setIsDemo] = useState(false);
  const [copied, setCopied] = useState(false);
  const [consented, setConsented] = useState(false);

  const activeQuestion = analysis?.questions[questionIndex];

  useEffect(() => {
    const context = document.modelContext;
    if (!context?.registerTool) return;
    const lifecycle = new AbortController();
    const click = (selector: string) => {
      const button = document.querySelector<HTMLButtonElement>(selector);
      if (!button) throw new Error("현재 화면에서는 이 동작을 사용할 수 없습니다.");
      button.click();
    };
    const requireEmptyInput = (input: unknown) => {
      if (!input || typeof input !== "object" || Array.isArray(input) || Object.keys(input).length > 0) {
        throw new Error("이 도구는 입력값을 받지 않습니다.");
      }
    };

    const registrations = [
      context.registerTool({
        name: "get_reflection_state",
        title: "기록 상태 확인",
        description: "현재 사진 기억 인터뷰의 단계와 선택된 사진 수, 샘플 여부를 확인합니다.",
        inputSchema: { type: "object", properties: {}, additionalProperties: false },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input) { requireEmptyInput(input); return { stage, photoCount: photos.length, isDemo }; },
      }, { signal: lifecycle.signal }),
      context.registerTool({
        name: "start_new_reflection",
        title: "새 기록 시작",
        description: "현재 브라우저의 사진, 답변, 결과를 지우고 새 사진 기록 시작 화면으로 돌아갑니다.",
        inputSchema: { type: "object", properties: {}, additionalProperties: false },
        annotations: { readOnlyHint: false, untrustedContentHint: false },
        execute(input) { requireEmptyInput(input); click('[data-webmcp-action="reset"]'); return { stage: "upload", cleared: true }; },
      }, { signal: lifecycle.signal }),
      ...(stage === "upload" ? [context.registerTool({
        name: "show_sample_record",
        title: "샘플 기록 보기",
        description: "개인 사진을 올리지 않고 근거가 표시된 완성 기록의 샘플 화면을 엽니다.",
        inputSchema: { type: "object", properties: {}, additionalProperties: false },
        annotations: { readOnlyHint: false, untrustedContentHint: false },
        execute(input) { requireEmptyInput(input); click('[data-webmcp-action="show-sample"]'); return { stage: "result", isDemo: true }; },
      }, { signal: lifecycle.signal })] : []),
    ];

    void Promise.all(registrations.map((registration) => Promise.resolve(registration))).catch((error) => console.warn("WebMCP registration failed", error));
    return () => lifecycle.abort();
  }, [stage, photos.length, isDemo]);

  function moveTo(next: Stage) {
    setStage(next);
    setMessage("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function addFiles(fileList: FileList | File[]) {
    const imageFiles = Array.from(fileList).filter((file) => ["image/jpeg", "image/png", "image/webp"].includes(file.type));
    if (!imageFiles.length) {
      setMessage("JPG, PNG 또는 WEBP 사진을 선택해 주세요.");
      return;
    }

    const available = MAX_PHOTOS - photos.length;
    if (available <= 0) {
      setMessage("사진은 최대 8장까지 올릴 수 있어요.");
      return;
    }

    setPending("prepare");
    setMessage("");
    setIsDemo(false);

    try {
      const next = await Promise.all(imageFiles.slice(0, available).map(removeMetadata));
      setPhotos((current) => [...current, ...next].sort((a, b) => a.time - b.time));
      if (imageFiles.length > available) setMessage(`최대 8장까지만 담았어요. ${imageFiles.length - available}장은 제외했습니다.`);
    } catch {
      setMessage("일부 사진을 준비하지 못했습니다. 다른 사진으로 다시 시도해 주세요.");
    } finally {
      setPending(null);
      if (fileInput.current) fileInput.current.value = "";
    }
  }

  function removePhoto(clientId: string) {
    setPhotos((current) => current.filter((photo) => photo.clientId !== clientId));
    setMessage("");
  }

  async function runAnalysis() {
    if (photos.length < 3) return;
    setPending("analyze");
    setMessage("");

    try {
      const value = await postReflection({
        action: "analyze",
        photos: photos.map((photo, index) => ({
          id: photoId(index),
          capturedAt: new Date(photo.time).toISOString(),
          imageUrl: photo.dataUrl,
        })),
      });
      setAnalysis(value.analysis);
      setQuestionIndex(0);
      moveTo("interview");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "사진 분석을 완료하지 못했습니다.");
    } finally {
      setPending(null);
    }
  }

  async function composeRecord(nextAnswers: string[]) {
    if (!analysis) return;
    setPending("compose");
    setMessage("");

    const answerPayload: ReflectionAnswer[] = nextAnswers.map((text, index) => ({
      id: `U0${index + 1}`,
      questionId: `Q0${index + 1}`,
      text: text.trim(),
      skipped: !text.trim(),
    }));

    try {
      const value = await postReflection({
        action: "compose",
        analysis,
        answers: answerPayload,
        photoIds: photos.map((_, index) => photoId(index)),
      });
      setDiary(value.diary);
      setSourceFocus(value.diary.sentences[0]?.sources[0] || null);
      moveTo("result");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "기록을 완성하지 못했습니다.");
    } finally {
      setPending(null);
    }
  }

  async function continueInterview(skip = false) {
    const nextAnswers = [...answers];
    if (skip) nextAnswers[questionIndex] = "";
    setAnswers(nextAnswers);

    if (questionIndex < 2) {
      setQuestionIndex((current) => current + 1);
      setMessage("");
      return;
    }
    await composeRecord(nextAnswers);
  }

  function loadDemo() {
    setPhotos(demoPhotos);
    setAnalysis(demoAnalysis);
    setAnswers(demoAnswers);
    setDiary(demoDiary);
    setSourceFocus("P01");
    setIsDemo(true);
    moveTo("result");
  }

  function resetAll() {
    setStage("upload");
    setPhotos([]);
    setAnalysis(null);
    setAnswers(["", "", ""]);
    setQuestionIndex(0);
    setDiary(null);
    setSourceFocus(null);
    setMessage("");
    setPending(null);
    setIsDemo(false);
    setCopied(false);
    setConsented(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function recordText() {
    if (!diary) return "";
    return `${diary.title}\n\n${diary.sentences.map((sentence) => sentence.text).join(" ")}`;
  }

  async function copyRecord() {
    await navigator.clipboard.writeText(recordText());
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  function downloadRecord() {
    const blob = new Blob([recordText()], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "사진이-묻는-하루.txt";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  function sourceDescription(source: string | null) {
    if (!source) return null;
    if (source.startsWith("P")) {
      const index = Number(source.slice(1)) - 1;
      return { icon: <Eye />, label: `${source} · 사진에서 본 것`, text: analysis?.moments.find((moment) => moment.photoIds.includes(source))?.observation || "이 문장에 연결된 사진입니다.", photo: photos[index] };
    }
    if (source.startsWith("U")) {
      const index = Number(source.slice(1)) - 1;
      return { icon: <MessageCircle />, label: `${source} · 내가 답한 말`, text: answers[index] || "이 질문은 건너뛰었습니다.", photo: null };
    }
    if (source === "TIME") return { icon: <Clock3 />, label: "TIME · 사진 순서", text: "브라우저가 읽은 파일 시간을 기준으로 정렬한 순서입니다.", photo: null };
    return { icon: <Sparkles />, label: "AI_STYLE · 표현 정리", text: "새 사실을 더하지 않고 문장의 연결과 표현만 다듬었습니다.", photo: null };
  }

  const focusedSource = sourceDescription(sourceFocus);

  return (
    <main className="min-h-screen bg-[var(--paper)] text-[var(--ink)]" data-stage={stage} data-photo-count={photos.length} data-demo={isDemo}>
      <header className="border-b border-[var(--line)] px-5 py-4 sm:px-8 lg:px-12">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between gap-4">
          <button className="group flex items-center gap-3" onClick={resetAll} aria-label="처음으로 돌아가기" data-webmcp-action="reset">
            <span className="brand-mark" aria-hidden="true"><span /><span /><span /></span>
            <span className="text-[15px] font-extrabold tracking-[-0.03em]">사진이 묻는 하루</span>
          </button>
          <div className="flex items-center gap-2 text-xs font-semibold text-[var(--soft-ink)]">
            <LockKeyhole className="size-3.5" aria-hidden="true" />
            <span className="hidden sm:inline">원본 사진은 저장하지 않아요</span>
            <span className="sm:hidden">원본 미저장</span>
          </div>
        </div>
      </header>

      <section className="mx-auto grid max-w-[1440px] gap-10 px-5 py-10 sm:px-8 lg:grid-cols-[0.72fr_1.28fr] lg:gap-16 lg:px-12 lg:py-16">
        <aside className="flex flex-col justify-between gap-12 lg:min-h-[680px]">
          <div>
            <p className="eyebrow"><Sparkles className="size-3.5" /> AI 기억 인터뷰</p>
            {stage === "upload" && (
              <>
                <h1 className="mt-6 max-w-[520px] text-[clamp(2.8rem,6.2vw,6.4rem)] font-black leading-[0.93] tracking-[-0.075em]">이 사진들,<br />왜<br /><span className="title-accent">남겼을까?</span></h1>
                <p className="mt-8 max-w-md text-base font-medium leading-7 text-[var(--soft-ink)] sm:text-lg">흩어진 사진을 시간순으로 펼치고, AI가 기억을 되살리는 질문 세 개를 건넵니다. 답하고 나면 사진과 내 말에만 근거한 오늘의 기록이 남아요.</p>
              </>
            )}
            {stage === "interview" && (
              <>
                <p className="section-number">0{questionIndex + 1}</p>
                <h1 className="mt-4 max-w-[500px] text-[clamp(2.6rem,5vw,5rem)] font-black leading-[.98] tracking-[-0.065em]">사진 밖의<br /><span className="title-accent">기억</span>을 묻다.</h1>
                <p className="mt-7 max-w-md text-base font-medium leading-7 text-[var(--soft-ink)]">사진 속 사실을 맞히는 대신, 사진만으로는 알 수 없는 당신의 하루를 기다립니다.</p>
              </>
            )}
            {stage === "result" && (
              <>
                <p className="section-number"><Check /></p>
                <h1 className="mt-4 max-w-[500px] text-[clamp(2.6rem,5vw,5rem)] font-black leading-[.98] tracking-[-0.065em]">기억에<br /><span className="title-accent">근거</span>를 남기다.</h1>
                <p className="mt-7 max-w-md text-base font-medium leading-7 text-[var(--soft-ink)]">근거 표식을 누르면 이 문장이 어느 사진과 답변에서 왔는지 바로 확인할 수 있어요.</p>
              </>
            )}
          </div>

          <ol className="process-list" aria-label="기록 만들기 순서">
            {["사진 고르기", "기억 대화하기", "기록 남기기"].map((label, index) => {
              const current = stage === "upload" ? 0 : stage === "interview" ? 1 : 2;
              return <li key={label} className={index === current ? "active" : index < current ? "done" : ""}><span>0{index + 1}</span><strong>{label}</strong>{index < current && <Check />}</li>;
            })}
          </ol>
        </aside>

        {stage === "upload" && (
          <section className="workbench" aria-labelledby="upload-title">
            <div className="workbench-head">
              <div><p className="micro-label">New reflection</p><h2 id="upload-title" className="workbench-title">오늘을 보여줄 사진을 골라주세요</h2></div>
              <span className="counter" aria-label={`${photos.length}장 선택됨`}>{String(photos.length).padStart(2, "0")} / 08</span>
            </div>

            <input ref={fileInput} className="sr-only" type="file" accept="image/jpeg,image/png,image/webp" multiple onChange={(event) => event.target.files && addFiles(event.target.files)} />

            {photos.length === 0 ? (
              <div className={`drop-zone ${isDragging ? "is-dragging" : ""}`} onDragEnter={(event) => { event.preventDefault(); setIsDragging(true); }} onDragOver={(event) => event.preventDefault()} onDragLeave={() => setIsDragging(false)} onDrop={(event) => { event.preventDefault(); setIsDragging(false); addFiles(event.dataTransfer.files); }}>
                <div className="drop-icon"><ImagePlus className="size-9" strokeWidth={1.6} /></div>
                <p className="mt-6 text-xl font-black tracking-[-0.035em]">3–8장을 한 번에 올려보세요</p>
                <p className="mt-2 max-w-sm text-sm leading-6 text-[var(--soft-ink)]">파일 시간을 기준으로 먼저 정리합니다. 시간 정보가 같으면 선택한 순서를 따를게요.</p>
                <Button className="mt-7 h-11 rounded-full bg-[var(--ink)] px-6 text-[var(--paper)] hover:bg-[var(--ink)]/88" onClick={() => fileInput.current?.click()} disabled={pending !== null}><Images /> {pending === "prepare" ? "사진 준비 중…" : "사진 선택하기"}</Button>
                <p className="mt-4 font-mono text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--faint-ink)]">JPG · PNG · WEBP / 최대 8장</p>
              </div>
            ) : (
              <ContactSheet photos={photos} removable onRemove={removePhoto} onAdd={() => fileInput.current?.click()} pending={pending === "prepare"} />
            )}

            <div className="workbench-foot">
              <div className="consent-block">
                <Checkbox id="photo-consent" checked={consented} onCheckedChange={(checked) => setConsented(checked === true)} />
                <label htmlFor="photo-consent"><strong>축소·메타데이터 제거 사본을 OpenAI API로 보내는 데 동의합니다.</strong><br />응답 저장은 끄지만 정책에 따라 안전 로그가 최대 30일 유지될 수 있어요.</label>
              </div>
              <div className="flex flex-col items-stretch gap-2 sm:items-end">
                <Button className="h-12 rounded-full bg-[var(--coral)] px-6 font-extrabold text-white hover:bg-[var(--coral-dark)]" disabled={photos.length < 3 || !consented || pending !== null} onClick={runAnalysis}>
                  {pending === "analyze" ? <><LoaderCircle className="animate-spin" /> 사진을 살펴보는 중…</> : <>AI와 돌아보기 <ArrowRight /></>}
                </Button>
                <button className="sample-link" onClick={loadDemo} data-webmcp-action="show-sample">예시 사진 4장으로 결과 보기</button>
              </div>
            </div>
            <p className={`status-line ${message ? "visible" : ""}`} role="status">{message || "사진을 준비하는 중입니다."}</p>
          </section>
        )}

        {stage === "interview" && analysis && activeQuestion && (
          <section className="workbench interview-bench" aria-labelledby="question-title">
            <div className="workbench-head">
              <div><p className="micro-label">Memory interview · {questionIndex + 1} of 3</p><h2 id="question-title" className="workbench-title">{analysis.timelineTitle}</h2></div>
              <span className="counter">Q 0{questionIndex + 1}</span>
            </div>

            <div className="interview-grid">
              <div className="timeline-panel">
                <p className="panel-label"><Eye /> 사진에서 본 것 / 아직 모르는 것</p>
                <div className="timeline-list">
                  {analysis.moments.map((moment) => (
                    <article key={moment.id} className="moment-card">
                      <div className="moment-meta"><time>{moment.label}</time><span>{moment.photoIds.join(" · ")}</span></div>
                      <p className="observation">{moment.observation}</p>
                      <p className="unknown"><span>?</span>{moment.unknown}</p>
                    </article>
                  ))}
                </div>
              </div>

              <div className="question-panel">
                <div>
                  <span className="intent-badge">{activeQuestion.intent}</span>
                  <h3 className="question-text">{activeQuestion.text}</h3>
                  <div className="question-sources">{activeQuestion.photoIds.map((id) => <span key={id}>{id}</span>)}</div>
                </div>
                <Textarea className="answer-box" placeholder="떠오르는 만큼만 편하게 적어주세요." value={answers[questionIndex]} maxLength={1200} onChange={(event) => setAnswers((current) => current.map((answer, index) => index === questionIndex ? event.target.value : answer))} disabled={pending !== null} />
                <div className="question-actions">
                  <button className="text-button" onClick={() => questionIndex > 0 && setQuestionIndex((current) => current - 1)} disabled={questionIndex === 0 || pending !== null}><ArrowLeft /> 이전</button>
                  <div className="flex items-center gap-2">
                    <button className="text-button" onClick={() => continueInterview(true)} disabled={pending !== null}>건너뛰기</button>
                    <Button className="h-11 rounded-full bg-[var(--coral)] px-5 font-extrabold text-white hover:bg-[var(--coral-dark)]" onClick={() => continueInterview(false)} disabled={!answers[questionIndex].trim() || pending !== null}>
                      {pending === "compose" ? <><LoaderCircle className="animate-spin" /> 기록 엮는 중…</> : questionIndex === 2 ? <>기록 완성하기 <Sparkles /></> : <>다음 질문 <ArrowRight /></>}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
            <p className={`status-line ${message ? "visible" : ""}`} role="status">{message || "답변을 기다리고 있습니다."}</p>
          </section>
        )}

        {stage === "result" && diary && analysis && (
          <section className="workbench result-bench" aria-labelledby="record-title">
            <div className="workbench-head">
              <div><p className="micro-label">Grounded record</p><h2 id="record-title" className="workbench-title">사진과 내 말로 만든 기록</h2></div>
              {isDemo && <span className="demo-stamp">SAMPLE</span>}
            </div>

            {isDemo && <div className="demo-notice">AI로 제작한 예시 사진과 고정된 예시 결과입니다. 실제 사진 분석 결과가 아닙니다.</div>}

            <div className="result-grid">
              <article className="diary-paper">
                <p className="diary-date">{new Intl.DateTimeFormat("ko-KR", { dateStyle: "long" }).format(photos[0]?.time || 0)}</p>
                <h3>{diary.title}</h3>
                <div className="sentence-list">
                  {diary.sentences.map((sentence) => (
                    <div className="sentence" key={sentence.id}>
                      <p>{sentence.text}</p>
                      <div className="source-chips" aria-label={`${sentence.id} 문장의 근거`}>
                        {sentence.sources.map((source) => <button key={source} className={sourceFocus === source ? "selected" : ""} onClick={() => setSourceFocus(source)}>{source}</button>)}
                      </div>
                    </div>
                  ))}
                </div>
              </article>

              <aside className="evidence-panel">
                <p className="panel-label"><Sparkles /> 이 문장은 어디에서 왔을까?</p>
                {focusedSource && (
                  <div className="evidence-card">
                    {focusedSource.photo && <img src={focusedSource.photo.dataUrl} alt={`${sourceFocus} 근거 사진`} />}
                    <div className="evidence-copy"><span>{focusedSource.icon}</span><strong>{focusedSource.label}</strong><p>{focusedSource.text}</p></div>
                  </div>
                )}
                <div className="evidence-legend"><p><span className="dot photo" /> PHOTO — 사진에서 직접 본 장면</p><p><span className="dot user" /> USER — 질문에 내가 답한 말</p><p><span className="dot time" /> TIME — 파일 시간의 순서</p><p><span className="dot style" /> AI_STYLE — 사실 추가 없는 표현 정리</p></div>
              </aside>
            </div>

            <div className="result-actions">
              <Button variant="outline" className="rounded-full border-[var(--ink)] bg-transparent" onClick={resetAll}><RotateCcw /> 새 기록</Button>
              <div className="flex gap-2">
                <Button variant="outline" className="rounded-full border-[var(--ink)] bg-transparent" onClick={copyRecord}>{copied ? <Check /> : <Copy />} {copied ? "복사됨" : "복사"}</Button>
                <Button className="rounded-full bg-[var(--ink)] text-[var(--paper)] hover:bg-[var(--ink)]/88" onClick={downloadRecord}><Download /> TXT 저장</Button>
              </div>
            </div>
          </section>
        )}
      </section>
    </main>
  );
}

function ContactSheet({ photos, removable, onRemove, onAdd, pending }: { photos: LocalPhoto[]; removable?: boolean; onRemove?: (clientId: string) => void; onAdd?: () => void; pending?: boolean }) {
  return (
    <div className="contact-sheet">
      {photos.map((photo, index) => (
        <figure key={photo.clientId} className="photo-frame">
          {/* Data URLs are generated in-browser after canvas re-encoding. */}
          <img src={photo.dataUrl} alt={`선택한 사진 ${index + 1}`} />
          <figcaption><span>{photoId(index)}</span><time dateTime={new Date(photo.time).toISOString()}>{new Intl.DateTimeFormat("ko-KR", { hour: "2-digit", minute: "2-digit" }).format(photo.time)}</time></figcaption>
          {removable && onRemove && <button className="remove-photo" onClick={() => onRemove(photo.clientId)} aria-label={`${index + 1}번 사진 빼기`}><X /></button>}
        </figure>
      ))}
      {removable && photos.length < MAX_PHOTOS && <button className="add-tile" onClick={onAdd} disabled={pending}><ImagePlus /><span>{pending ? "준비 중…" : "더 담기"}</span></button>}
    </div>
  );
}
