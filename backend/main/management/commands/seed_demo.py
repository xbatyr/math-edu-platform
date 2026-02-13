from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from main.models import Course, Lesson, Module, Problem


class Command(BaseCommand):
    help = "Seed demo data for math educational platform"

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            slug="podgotovka-k-nish-i-rfmsh",
            defaults={
                "title": "Подготовка к НИШ и РФМШ по математике",
                "description": "Интенсивная подготовка по алгебре и геометрии.",
                "cover_image": "https://images.example.com/math-course-cover.jpg",
                "is_published": True,
            },
        )

        modules_data = [
            {
                "title": "Алгебра: линейные уравнения",
                "order": 1,
                "description": "Базовые линейные уравнения и текстовые задачи",
                "lesson": {
                    "title": "Линейные уравнения и пропорции",
                    "video_url": "https://example.com/videos/linear-equations",
                    "content": "Разбираем переносы, пропорции и типовые экзаменационные шаблоны.",
                    "duration_minutes": 35,
                    "problems": [
                        ("Решите: 2x + 5 = 17", "6", "Выразите x через свободный член."),
                        ("Решите: 3(x - 2) = 9", "5", "Раскройте скобки и разделите обе части на 3."),
                        ("Найдите x: x/4 = 3", "12", "Умножьте обе части на 4."),
                    ],
                },
            },
            {
                "title": "Геометрия: углы и треугольники",
                "order": 2,
                "description": "Основные свойства углов и треугольников",
                "lesson": {
                    "title": "Сумма углов треугольника",
                    "video_url": "https://example.com/videos/triangle-angles",
                    "content": "Тренируемся применять сумму углов и свойства равнобедренного треугольника.",
                    "duration_minutes": 40,
                    "problems": [
                        ("В треугольнике два угла 50 и 60. Найдите третий угол.", "70", "Сумма углов треугольника равна 180."),
                        ("У равнобедренного треугольника угол при вершине 40. Найдите угол у основания.", "70", "Основания углы равны и в сумме дают 140."),
                        ("Внешний угол треугольника равен 120, один удаленный внутренний угол 50. Найдите второй.", "70", "Внешний угол равен сумме удаленных внутренних."),
                    ],
                },
            },
        ]

        for module_data in modules_data:
            module, _ = Module.objects.get_or_create(
                course=course,
                order=module_data["order"],
                defaults={
                    "title": module_data["title"],
                    "description": module_data["description"],
                },
            )
            lesson_data = module_data["lesson"]
            lesson, _ = Lesson.objects.get_or_create(
                module=module,
                order=1,
                defaults={
                    "title": lesson_data["title"],
                    "video_url": lesson_data["video_url"],
                    "content": lesson_data["content"],
                    "duration_minutes": lesson_data["duration_minutes"],
                },
            )

            for idx, (prompt, answer, explanation) in enumerate(lesson_data["problems"], start=1):
                Problem.objects.get_or_create(
                    lesson=lesson,
                    order=idx,
                    defaults={
                        "prompt": prompt,
                        "correct_answer": answer,
                        "explanation": explanation,
                        "points": 1,
                    },
                )

        if not User.objects.filter(username="student").exists():
            User.objects.create_user(username="student", password="student12345", email="student@example.com")

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
