import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import type { CourseDetail, CourseTree } from "@/types/api";

export function CourseDetailPage() {
  const { courseId = "" } = useParams();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [tree, setTree] = useState<CourseTree | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    Promise.all([
      api.get<CourseDetail>(`/courses/${courseId}/`),
      api.get<CourseTree>(`/courses/${courseId}/tree/`),
    ])
      .then(([courseRes, treeRes]) => {
        setCourse(courseRes.data);
        setTree(treeRes.data);
      })
      .catch(() => setError("Failed to load course."));
  }, [courseId]);

  const enroll = async () => {
    try {
      await api.post(`/courses/${courseId}/enroll/`);
      const updatedTree = await api.get<CourseTree>(`/courses/${courseId}/tree/`);
      setTree(updatedTree.data);
    } catch {
      setError("Login required for enrollment.");
    }
  };

  if (!course) return <main className="mx-auto max-w-4xl p-6">Loading...</main>;

  return (
    <main className="mx-auto max-w-5xl space-y-6 p-6">
      <Card className="animate-fade-up bg-foreground text-background">
        <CardContent className="space-y-4 p-8">
          <h1 className="text-4xl">{course.title}</h1>
          <p className="max-w-3xl text-sm text-slate-200">{course.description}</p>
          {tree && (
            <div className="max-w-md space-y-2">
              <div className="flex justify-between text-sm">
                <span>Progress</span>
                <span>{tree.course_progress}%</span>
              </div>
              <Progress value={tree.course_progress} className="bg-slate-700" />
            </div>
          )}
          <div className="flex gap-3">
            <Button onClick={enroll}>Enroll</Button>
            <Link to={`/learn/${courseId}/1`}>
              <Button variant="outline">Open Learn</Button>
            </Link>
          </div>
          {!isAuthenticated && <p className="text-xs text-slate-300">Login to enroll and save progress.</p>}
          {error && <p className="text-sm text-amber-300">{error}</p>}
        </CardContent>
      </Card>

      <section className="space-y-4">
        <h2 className="text-2xl">Course Tree</h2>
        {tree?.modules.map((module) => (
          <Card key={module.id}>
            <CardContent className="space-y-3">
              <h3 className="text-xl">{module.title}</h3>
              <p className="text-sm text-muted-foreground">{module.description}</p>
              <div className="space-y-2">
                {module.lessons.map((lesson) => (
                  <Link
                    key={lesson.id}
                    to={`/learn/${courseId}/${lesson.id}`}
                    className="flex items-center justify-between rounded-lg border border-border px-3 py-2 text-sm hover:bg-muted"
                  >
                    <span>{lesson.title}</span>
                    <span>{lesson.lesson_completed ? "Done" : `${lesson.duration_minutes} min`}</span>
                  </Link>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </section>
    </main>
  );
}
