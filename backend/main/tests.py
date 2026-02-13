from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Course, Enrollment, Lesson, Module, Problem


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="strongpass123", email="t@example.com")

        self.course = Course.objects.create(
            title="Подготовка к НИШ и РФМШ по математике",
            slug="nish-rfmsh",
            description="Демо курс",
            is_published=True,
        )
        self.module = Module.objects.create(course=self.course, title="Модуль 1", order=1)
        self.lesson = Lesson.objects.create(
            module=self.module,
            title="Урок 1",
            order=1,
            video_url="https://example.com/video1",
            content="Контент",
        )
        self.problem = Problem.objects.create(
            lesson=self.lesson,
            order=1,
            prompt="2+2?",
            correct_answer="4",
            explanation="Сложение",
            points=1,
        )

    def _login_and_get_access(self):
        response = self.client.post(
            reverse("auth-login"),
            data={"username": "tester", "password": "strongpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        return response.data["access"], response.data["refresh"]

    def test_register_login_refresh(self):
        register = self.client.post(
            reverse("auth-register"),
            data={"username": "newuser", "email": "new@example.com", "password": "verystrong123"},
            format="json",
        )
        self.assertEqual(register.status_code, 201)
        self.assertIn("access", register.data)
        self.assertIn("refresh", register.data)

        invalid_login = self.client.post(
            reverse("auth-login"),
            data={"username": "newuser", "password": "wrong"},
            format="json",
        )
        self.assertEqual(invalid_login.status_code, 401)

        valid_login = self.client.post(
            reverse("auth-login"),
            data={"username": "newuser", "password": "verystrong123"},
            format="json",
        )
        self.assertEqual(valid_login.status_code, 200)

        refreshed = self.client.post(
            reverse("auth-refresh"),
            data={"refresh": valid_login.data["refresh"]},
            format="json",
        )
        self.assertEqual(refreshed.status_code, 200)
        self.assertIn("access", refreshed.data)

    def test_courses_list_and_detail_public(self):
        response = self.client.get(reverse("courses-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        detail_by_id = self.client.get(reverse("courses-detail", kwargs={"course_ref": str(self.course.id)}))
        self.assertEqual(detail_by_id.status_code, 200)

        detail_by_slug = self.client.get(reverse("courses-detail", kwargs={"course_ref": self.course.slug}))
        self.assertEqual(detail_by_slug.status_code, 200)

    def test_enroll_idempotent(self):
        access, _ = self._login_and_get_access()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        first = self.client.post(reverse("courses-enroll", kwargs={"course_id": self.course.id}), format="json")
        second = self.client.post(reverse("courses-enroll", kwargs={"course_id": self.course.id}), format="json")

        self.assertIn(first.status_code, [200, 201])
        self.assertIn(second.status_code, [200, 201])
        self.assertEqual(Enrollment.objects.filter(user=self.user, course=self.course).count(), 1)

    def test_course_tree_structure(self):
        response = self.client.get(reverse("courses-tree", kwargs={"course_id": self.course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["modules"]), 1)
        self.assertEqual(len(response.data["modules"][0]["lessons"]), 1)

    def test_lesson_detail_hides_correct_answer(self):
        response = self.client.get(reverse("lessons-detail", kwargs={"pk": self.lesson.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("problems", response.data)
        self.assertNotIn("correct_answer", response.data["problems"][0])

    def test_attempt_submit_and_progress(self):
        access, _ = self._login_and_get_access()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        self.client.post(reverse("courses-enroll", kwargs={"course_id": self.course.id}), format="json")

        wrong = self.client.post(
            reverse("attempt-submit"),
            data={"problem_id": self.problem.id, "answer": "5"},
            format="json",
        )
        self.assertEqual(wrong.status_code, 201)
        self.assertFalse(wrong.data["is_correct"])
        self.assertEqual(wrong.data["course_progress"], 0)
        self.assertEqual(wrong.data["correct_answer_if_wrong"], "4")

        correct = self.client.post(
            reverse("attempt-submit"),
            data={"problem_id": self.problem.id, "answer": "4"},
            format="json",
        )
        self.assertEqual(correct.status_code, 201)
        self.assertTrue(correct.data["is_correct"])
        self.assertEqual(correct.data["course_progress"], 100)

    def test_seed_command(self):
        Course.objects.filter(slug="podgotovka-k-nish-i-rfmsh").delete()
        call_command("seed_demo")
        self.assertEqual(Course.objects.filter(slug="podgotovka-k-nish-i-rfmsh").count(), 1)
        seeded = Course.objects.get(slug="podgotovka-k-nish-i-rfmsh")
        self.assertEqual(Module.objects.filter(course=seeded).count(), 2)
        self.assertEqual(Lesson.objects.filter(module__course=seeded).count(), 2)
        self.assertEqual(Problem.objects.filter(lesson__module__course=seeded).count(), 6)
