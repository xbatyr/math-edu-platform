export type UserDto = {
  id: number;
  username: string;
  email: string;
};

export type AuthResponse = {
  access: string;
  refresh: string;
  user: UserDto;
};

export type CourseListItem = {
  id: number;
  slug: string;
  title: string;
  description: string;
  cover_image: string;
  modules_count: number;
  lessons_count: number;
  enrolled: boolean;
  progress_percent: number;
};

export type CourseDetail = {
  id: number;
  slug: string;
  title: string;
  description: string;
  cover_image: string;
  is_published: boolean;
  modules_count: number;
  lessons_count: number;
};

export type LessonTreeNode = {
  id: number;
  title: string;
  order: number;
  duration_minutes: number;
  lesson_completed: boolean;
};

export type ModuleTreeNode = {
  id: number;
  title: string;
  order: number;
  description: string;
  lessons: LessonTreeNode[];
};

export type CourseTree = {
  course: CourseDetail;
  modules: ModuleTreeNode[];
  course_progress: number;
};

export type ProblemPublic = {
  id: number;
  order: number;
  prompt: string;
  explanation: string;
  points: number;
};

export type LessonDetail = {
  id: number;
  module_id: number;
  course_id: number;
  title: string;
  order: number;
  video_url: string;
  content: string;
  duration_minutes: number;
  problems: ProblemPublic[];
};

export type AttemptResult = {
  attempt_id: number;
  is_correct: boolean;
  awarded_points: number;
  lesson_progress: number;
  course_progress: number;
  correct_answer_if_wrong: string | null;
};

export type Enrollment = {
  id: number;
  progress_percent: number;
  created_at: string;
  course: CourseListItem;
};
