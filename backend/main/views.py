from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Course, Enrollment, Lesson, Problem
from .serializers import (
    AttemptResultSerializer,
    AttemptSubmitSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    CourseTreeSerializer,
    EnrollResponseSerializer,
    EnrollmentSerializer,
    LessonDetailSerializer,
    RegisterSerializer,
    UserSerializer,
)
from .services import compute_course_progress, compute_lesson_completion, grade_attempt, upsert_enrollment_progress


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok", "service": "math-edu-backend"})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer
    permission_classes = [permissions.AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return (
            Course.objects.filter(is_published=True)
            .annotate(
                modules_count=Count("modules", distinct=True),
                lessons_count=Count("modules__lessons", distinct=True),
            )
            .order_by("title")
        )


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        course_ref = self.kwargs["course_ref"]
        queryset = Course.objects.filter(is_published=True)
        if course_ref.isdigit():
            return get_object_or_404(queryset, id=int(course_ref))
        return get_object_or_404(queryset, slug=course_ref)


class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, is_published=True)
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        enrollment = upsert_enrollment_progress(request.user, course)
        serializer = EnrollResponseSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class CourseTreeView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, course_id):
        course = get_object_or_404(Course.objects.prefetch_related("modules__lessons"), id=course_id, is_published=True)
        progress = compute_course_progress(request.user, course) if request.user.is_authenticated else 0
        payload = {
            "course": CourseDetailSerializer(course).data,
            "modules": CourseTreeSerializer(context={"request": request}).get_modules(course),
            "course_progress": progress,
        }
        return Response(payload)


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.select_related("module", "module__course").prefetch_related("problems")
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.AllowAny]


class AttemptSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AttemptSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        problem = get_object_or_404(Problem.objects.select_related("lesson", "lesson__module", "lesson__module__course"), id=serializer.validated_data["problem_id"])
        attempt = grade_attempt(request.user, problem, serializer.validated_data["answer"])

        lesson = problem.lesson
        course = lesson.module.course

        lesson_progress = 100 if compute_lesson_completion(request.user, lesson) else 0
        course_progress = compute_course_progress(request.user, course)

        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        if enrollment:
            enrollment.progress_percent = course_progress
            enrollment.save(update_fields=["progress_percent"])

        data = {
            "attempt_id": attempt.id,
            "is_correct": attempt.is_correct,
            "awarded_points": attempt.awarded_points,
            "lesson_progress": lesson_progress,
            "course_progress": course_progress,
            "correct_answer_if_wrong": None if attempt.is_correct else problem.correct_answer,
        }
        return Response(AttemptResultSerializer(data).data, status=status.HTTP_201_CREATED)


class MeEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Enrollment.objects.filter(user=self.request.user).select_related("course")
        for enrollment in qs:
            latest = compute_course_progress(self.request.user, enrollment.course)
            if enrollment.progress_percent != latest:
                enrollment.progress_percent = latest
                enrollment.save(update_fields=["progress_percent"])
        return qs
