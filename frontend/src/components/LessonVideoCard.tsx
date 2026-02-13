import { Card, CardContent } from "@/components/ui/card";

type Props = {
  title: string;
  videoUrl: string;
};

export function LessonVideoCard({ title, videoUrl }: Props) {
  return (
    <Card>
      <CardContent className="space-y-3">
        <h2 className="text-2xl font-semibold">{title}</h2>
        <div className="aspect-video overflow-hidden rounded-xl border border-border bg-muted">
          <iframe
            className="h-full w-full"
            src={videoUrl}
            title={title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
      </CardContent>
    </Card>
  );
}
