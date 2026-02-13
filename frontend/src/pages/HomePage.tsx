import { useEffect, useState } from "react";

import { CourseCard } from "@/components/CourseCard";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import type { CourseListItem } from "@/types/api";

export function HomePage() {
  const [courses, setCourses] = useState<CourseListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, logout } = useAuth();

  useEffect(() => {
    api
      .get<CourseListItem[]>("/courses/")
      .then(({ data }) => setCourses(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="mx-auto max-w-6xl space-y-8 px-4 py-8 md:px-6">
      <section className="editorial-panel animate-fade-up p-6 md:p-10">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="mb-2 text-xs uppercase tracking-[0.25em] text-muted-foreground">Math Editorial Track</p>
            <h1 className="text-4xl md:text-5xl">Build Competitive Math Confidence</h1>
            <p className="mt-3 max-w-2xl text-muted-foreground">
              Structured preparation for NIS and RFMSH with modules, lessons, and instant problem feedback.
            </p>
          </div>
          {user && (
            <div className="space-y-2 text-right">
              <p className="text-sm">Signed in as {user.username}</p>
              <Button variant="outline" onClick={logout}>
                Logout
              </Button>
            </div>
          )}
        </div>
      </section>

      <section>
        <h2 className="mb-4 text-2xl">Courses</h2>
        {loading && <p className="text-sm text-muted-foreground">Loading courses...</p>}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {courses.map((course) => (
            <CourseCard key={course.id} course={course} />
          ))}
        </div>
      </section>
    </main>
  );
}
