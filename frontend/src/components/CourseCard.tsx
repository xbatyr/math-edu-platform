import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { CourseListItem } from "@/types/api";

type Props = {
  course: CourseListItem;
};

export function CourseCard({ course }: Props) {
  return (
    <Card className="card-hover animate-fade-up">
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <Badge>{course.modules_count} modules</Badge>
          <span className="text-sm text-muted-foreground">{course.lessons_count} lessons</span>
        </div>

        <div>
          <h3 className="text-xl font-semibold">{course.title}</h3>
          <p className="mt-2 line-clamp-3 text-sm text-muted-foreground">{course.description}</p>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span>Progress</span>
            <span>{course.progress_percent}%</span>
          </div>
          <Progress value={course.progress_percent} />
        </div>

        <div className="flex gap-2">
          <Link to={`/courses/${course.id}`} className="w-full">
            <Button className="w-full" variant="outline">
              Details
            </Button>
          </Link>
          <Link to={`/learn/${course.id}/1`} className="w-full">
            <Button className="w-full">{course.enrolled ? "Continue" : "Learn"}</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
