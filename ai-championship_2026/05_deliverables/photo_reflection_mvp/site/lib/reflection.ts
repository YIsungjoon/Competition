export type PhotoInput = {
  id: string;
  capturedAt: string;
  imageUrl: string;
};

export type Moment = {
  id: string;
  label: string;
  observation: string;
  unknown: string;
  photoIds: string[];
};

export type ReflectionQuestion = {
  id: string;
  text: string;
  intent: string;
  photoIds: string[];
};

export type ReflectionAnalysis = {
  timelineTitle: string;
  moments: Moment[];
  questions: ReflectionQuestion[];
};

export type ReflectionAnswer = {
  id: string;
  questionId: string;
  text: string;
  skipped: boolean;
};

export type DiarySentence = {
  id: string;
  text: string;
  sources: string[];
};

export type DiaryResult = {
  title: string;
  sentences: DiarySentence[];
};

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function strings(value: unknown, minimum = 1): value is string[] {
  return Array.isArray(value) && value.length >= minimum && value.every((item) => typeof item === "string" && item.length > 0);
}

export function validateAnalysis(value: unknown, photoIds: Set<string>): ReflectionAnalysis {
  if (!isObject(value) || typeof value.timelineTitle !== "string" || !Array.isArray(value.moments) || !Array.isArray(value.questions)) {
    throw new Error("분석 응답 구조가 올바르지 않습니다.");
  }

  if (value.moments.length < 1 || value.moments.length > 8 || value.questions.length !== 3) {
    throw new Error("분석 응답 개수가 올바르지 않습니다.");
  }

  const moments = value.moments.map((moment) => {
    if (!isObject(moment) || typeof moment.id !== "string" || typeof moment.label !== "string" || typeof moment.observation !== "string" || typeof moment.unknown !== "string" || !strings(moment.photoIds)) {
      throw new Error("장면 응답 구조가 올바르지 않습니다.");
    }
    if (!moment.photoIds.every((id) => photoIds.has(id))) throw new Error("알 수 없는 사진 근거가 포함되었습니다.");
    return moment as Moment;
  });

  const questions = value.questions.map((question) => {
    if (!isObject(question) || typeof question.id !== "string" || typeof question.text !== "string" || typeof question.intent !== "string" || !strings(question.photoIds)) {
      throw new Error("질문 응답 구조가 올바르지 않습니다.");
    }
    if (!question.photoIds.every((id) => photoIds.has(id))) throw new Error("알 수 없는 질문 근거가 포함되었습니다.");
    return question as ReflectionQuestion;
  });

  return { timelineTitle: value.timelineTitle, moments, questions };
}

export function validateDiary(value: unknown, allowedSources: Set<string>): DiaryResult {
  if (!isObject(value) || typeof value.title !== "string" || !Array.isArray(value.sentences)) {
    throw new Error("기록 응답 구조가 올바르지 않습니다.");
  }
  if (value.sentences.length < 4 || value.sentences.length > 7) {
    throw new Error("기록은 4~7문장이어야 합니다.");
  }

  const sentences = value.sentences.map((sentence) => {
    if (!isObject(sentence) || typeof sentence.id !== "string" || typeof sentence.text !== "string" || !strings(sentence.sources)) {
      throw new Error("문장 근거가 비어 있습니다.");
    }
    if (!sentence.sources.every((source) => allowedSources.has(source))) {
      throw new Error("알 수 없는 문장 근거가 포함되었습니다.");
    }
    if (sentence.sources.every((source) => source === "AI_STYLE")) {
      throw new Error("문체만을 근거로 한 문장은 표시할 수 없습니다.");
    }
    return sentence as DiarySentence;
  });

  return { title: value.title, sentences };
}

export function extractResponseText(value: unknown): string {
  if (!isObject(value)) throw new Error("AI 응답을 읽지 못했습니다.");
  if (typeof value.output_text === "string" && value.output_text) return value.output_text;
  if (!Array.isArray(value.output)) throw new Error("AI 응답에 결과가 없습니다.");

  for (const item of value.output) {
    if (!isObject(item) || !Array.isArray(item.content)) continue;
    for (const content of item.content) {
      if (isObject(content) && content.type === "output_text" && typeof content.text === "string") return content.text;
    }
  }
  throw new Error("AI 응답에 텍스트 결과가 없습니다.");
}
