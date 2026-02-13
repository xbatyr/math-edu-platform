import { Link } from "react-router-dom";

import { cn } from "@/lib/utils";
import type { ModuleTreeNode } from "@/types/api";

type Props = {
  modules: ModuleTreeNode[];
  courseId: string;
  activeLessonId?: number;
};

export function ModuleTreeSidebar({ modules, courseId, activeLessonId }: Props) {
  return (
    <aside className="editorial-panel h-full p-4">
      <h3 className="mb-4 text-lg font-semibold">Course Map</h3>
      <div className="space-y-4">
        {modules.map((module) => (
          <div key={module.id} className="space-y-2">
            <p className="text-xs uppercase tracking-wide text-muted-foreground">{module.title}</p>
            <div className="space-y-1">
              {module.lessons.map((lesson) => (
                <Link
                  key={lesson.id}
                  to={`/learn/${courseId}/${lesson.id}`}
                  className={cn(
                    "flex items-center justify-between rounded-lg px-2 py-2 text-sm",
                    lesson.id === activeLessonId ? "bg-foreground text-background" : "hover:bg-muted"
                  )}
                >
                  <span>{lesson.title}</span>
                  <span className="text-xs">{lesson.lesson_completed ? "Done" : `${lesson.duration_minutes}m`}</span>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}
