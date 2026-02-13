import { BookOpen, LogIn } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

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

  const mainCourse = courses[0];

  return (
    <main className="min-h-screen bg-[#f5f7fe] text-slate-900">
      <header className="border-b border-slate-200 bg-white/95">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-8">
          <Link to="/" className="text-3xl font-extrabold tracking-tight text-[#2342c4]">
            VectorMath
          </Link>

          <nav className="hidden items-center gap-8 md:flex">
            <a className="flex items-center gap-2 text-base font-medium text-slate-600" href="#courses">
              <BookOpen size={18} /> Главная панель
            </a>
          </nav>

          <div className="flex items-center gap-2 md:gap-3">
            {user ? (
              <>
                <span className="hidden text-sm font-semibold text-slate-600 md:block">{user.username}</span>
                <Button variant="outline" onClick={logout} className="h-11 px-5">
                  Выйти
                </Button>
              </>
            ) : (
              <>
                <Link to="/login" className="hidden md:block">
                  <Button variant="ghost" className="h-11 px-5 text-base">
                    <LogIn size={16} className="mr-2" /> Войти
                  </Button>
                </Link>
                <Link to="/login">
                  <Button className="h-11 bg-[#2563eb] px-6 text-base text-white hover:bg-[#1e40af]">Регистрация</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      <section className="mx-auto flex max-w-5xl flex-col items-center px-4 pb-14 pt-16 text-center md:pt-20">
        <div className="mb-8 rounded-2xl border border-blue-200 bg-white px-7 py-3 text-lg font-medium text-[#2342c4]">
          VectorMath — персональная подготовка к поступлению
        </div>

        <h1 className="hero-modern-heading max-w-5xl text-4xl md:text-6xl">
          Мы VectorMath,
          <br />
          <span className="text-[#3b62bd]">все что тебе нужно</span>
          <br />
          для поступления в НИШ, РФМШ, БИЛ и другие топ-школы
        </h1>

        <p className="mt-6 max-w-3xl text-lg leading-relaxed text-slate-600 md:text-xl">
          Платформа для подготовки по математике: понятные уроки, практика, анализ ошибок и персональный маршрут
          к сильному результату на вступительных экзаменах.
        </p>

        <div className="mt-8 flex w-full max-w-3xl flex-col gap-4 sm:flex-row sm:justify-center">
          <Link to={mainCourse ? `/learn/${mainCourse.id}/1` : "/login"} className="w-full sm:w-auto">
            <Button className="h-14 w-full min-w-[300px] rounded-2xl bg-gradient-to-r from-[#1b3ea8] to-[#3a6af0] text-xl font-semibold text-white shadow-[0_10px_24px_rgba(37,99,235,0.22)] hover:brightness-105">
              Начать готовиться →
            </Button>
          </Link>
        </div>
      </section>

      <section id="courses" className="mx-auto max-w-7xl px-4 pb-16 md:px-8">
        <h2 className="mb-6 text-3xl font-bold">Курсы</h2>
        {loading && <p className="text-sm text-slate-500">Загрузка курсов...</p>}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {courses.map((course) => (
            <CourseCard key={course.id} course={course} />
          ))}
        </div>
      </section>
    </main>
  );
}
