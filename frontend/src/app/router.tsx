import { createBrowserRouter } from "react-router-dom";

import { CourseDetailPage } from "@/pages/CourseDetailPage";
import { HomePage } from "@/pages/HomePage";
import { LearnPage } from "@/pages/LearnPage";
import { LoginPage } from "@/pages/LoginPage";

export const router = createBrowserRouter([
  { path: "/", element: <HomePage /> },
  { path: "/login", element: <LoginPage /> },
  { path: "/courses/:courseId", element: <CourseDetailPage /> },
  { path: "/learn/:courseId/:lessonId", element: <LearnPage /> },
]);
