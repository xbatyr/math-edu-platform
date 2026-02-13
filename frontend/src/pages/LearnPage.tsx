import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { LessonVideoCard } from "@/components/LessonVideoCard";
import { ModuleTreeSidebar } from "@/components/ModuleTreeSidebar";
import { ProblemCard } from "@/components/ProblemCard";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import type { AttemptResult, CourseTree, LessonDetail } from "@/types/api";

export function LearnPage() {
  const { courseId = "", lessonId = "" } = useParams();
  const lessonNum = Number(lessonId);
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();

  const [tree, setTree] = useState<CourseTree | null>(null);
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (loading) {
      return;
    }

    if (!isAuthenticated) {
      navigate(`/login?next=/learn/${courseId}/${lessonId}`);
      return;
    }

    Promise.all([
      api.get<CourseTree>(`/courses/${courseId}/tree/`),
      api.get<LessonDetail>(`/lessons/${lessonId}/`),
    ]).then(([treeRes, lessonRes]) => {
      setTree(treeRes.data);
      setLesson(lessonRes.data);
    });
  }, [courseId, lessonId, isAuthenticated, loading, navigate]);

  const onAttemptResult = async (_result: AttemptResult) => {
    const refreshed = await api.get<CourseTree>(`/courses/${courseId}/tree/`);
    setTree(refreshed.data);
  };

  if (!tree || !lesson) return <main className="p-6">Loading lesson...</main>;

  return (
    <main className="grid min-h-screen grid-cols-1 gap-4 p-4 md:grid-cols-[320px_1fr]">
      <div className="md:hidden">
        <Button variant="outline" onClick={() => setMenuOpen((v) => !v)}>
          {menuOpen ? "Hide map" : "Show map"}
        </Button>
      </div>

      <div className={`${menuOpen ? "block" : "hidden"} md:block`}>
        <ModuleTreeSidebar modules={tree.modules} courseId={courseId} activeLessonId={lessonNum} />
      </div>

      <section className="space-y-4">
        <Card className="bg-foreground text-background">
          <CardContent className="space-y-3 p-6">
            <div className="flex items-center justify-between gap-3">
              <h1 className="text-3xl">{tree.course.title}</h1>
              <Link to={`/courses/${courseId}`}>
                <Button variant="outline">Course</Button>
              </Link>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-xs text-slate-300">
                <span>Course Progress</span>
                <span>{tree.course_progress}%</span>
              </div>
              <Progress value={tree.course_progress} className="bg-slate-700" />
            </div>
          </CardContent>
        </Card>

        <LessonVideoCard title={lesson.title} videoUrl={lesson.video_url} />

        <Card>
          <CardContent className="space-y-2">
            <h3 className="text-xl">Lesson content</h3>
            <p className="text-muted-foreground">{lesson.content}</p>
          </CardContent>
        </Card>

        <div className="space-y-3">
          {lesson.problems.map((problem) => (
            <ProblemCard key={problem.id} problem={problem} onResult={onAttemptResult} />
          ))}
        </div>
      </section>
    </main>
  );
}
