import { FormEvent, useState } from "react";

import { AttemptResultToast } from "@/components/AttemptResultToast";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import type { AttemptResult, ProblemPublic } from "@/types/api";

type Props = {
  problem: ProblemPublic;
  onResult: (result: AttemptResult) => void;
};

export function ProblemCard({ problem, onResult }: Props) {
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<AttemptResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const { data } = await api.post<AttemptResult>("/attempts/submit/", {
        problem_id: problem.id,
        answer,
      });
      setResult(data);
      onResult(data);
    } catch {
      setError("Failed to submit answer. Please login and try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card>
      <CardContent className="space-y-3">
        <div className="flex items-center justify-between">
          <h4 className="text-lg font-semibold">Task {problem.order}</h4>
          <span className="text-xs text-muted-foreground">{problem.points} pts</span>
        </div>
        <p>{problem.prompt}</p>
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Enter answer" required />
          <Button type="submit" disabled={submitting}>
            Submit
          </Button>
        </form>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <AttemptResultToast result={result} />
      </CardContent>
    </Card>
  );
}
