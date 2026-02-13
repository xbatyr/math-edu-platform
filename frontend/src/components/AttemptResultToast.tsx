import { CheckCircle2, XCircle } from "lucide-react";

import { cn } from "@/lib/utils";
import type { AttemptResult } from "@/types/api";

type Props = {
  result: AttemptResult | null;
};

export function AttemptResultToast({ result }: Props) {
  if (!result) return null;

  return (
    <div
      className={cn(
        "rounded-xl border p-3 text-sm",
        result.is_correct ? "border-emerald-300 bg-emerald-50 text-emerald-800" : "border-rose-300 bg-rose-50 text-rose-800"
      )}
    >
      <div className="flex items-center gap-2 font-medium">
        {result.is_correct ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
        {result.is_correct ? "Correct answer" : "Incorrect answer"}
      </div>
      <p className="mt-1">Lesson progress: {result.lesson_progress}% · Course progress: {result.course_progress}%</p>
      {!result.is_correct && result.correct_answer_if_wrong && (
        <p className="mt-1">Correct: {result.correct_answer_if_wrong}</p>
      )}
    </div>
  );
}
