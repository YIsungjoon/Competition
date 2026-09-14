import assert from "node:assert/strict";
import test from "node:test";

import { validateDiary } from "./reflection.ts";

const fourSentences = [1, 2, 3, 4].map((index) => ({
  id: `S0${index}`,
  text: `근거가 있는 문장 ${index}.`,
  sources: ["P01"],
}));

test("근거가 모두 허용된 4문장 기록을 통과시킨다", () => {
  const result = validateDiary({ title: "기록", sentences: fourSentences }, new Set(["P01", "AI_STYLE"]));
  assert.equal(result.sentences.length, 4);
});

test("AI_STYLE만 있는 문장은 거부한다", () => {
  const sentences = [...fourSentences];
  sentences[0] = { ...sentences[0], sources: ["AI_STYLE"] };
  assert.throws(() => validateDiary({ title: "기록", sentences }, new Set(["P01", "AI_STYLE"])), /문체만/);
});

test("알 수 없는 근거 ID를 거부한다", () => {
  const sentences = [...fourSentences];
  sentences[2] = { ...sentences[2], sources: ["U99"] };
  assert.throws(() => validateDiary({ title: "기록", sentences }, new Set(["P01", "AI_STYLE"])), /알 수 없는/);
});
