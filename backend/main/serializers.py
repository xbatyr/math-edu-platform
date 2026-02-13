from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Course, Enrollment, Lesson, Module, Problem
from .services import compute_course_progress, lesson_completion_map


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class AuthResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )


class CourseListSerializer(serializers.ModelSerializer):
    modules_count = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    enrolled = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "slug",
            "title",
            "description",
            "cover_image",
            "modules_count",
            "lessons_count",
            "enrolled",
            "progress_percent",
        )

    def get_enrolled(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Enrollment.objects.filter(user=request.user, course=obj).exists()

    def get_modules_count(self, obj):
        return getattr(obj, "modules_count", obj.modules.count())

    def get_lessons_count(self, obj):
        return getattr(obj, "lessons_count", Lesson.objects.filter(module__course=obj).count())

    def get_progress_percent(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        enrollment = Enrollment.objects.filter(user=request.user, course=obj).first()
        if enrollment:
            return enrollment.progress_percent
        return compute_course_progress(request.user, obj)


class CourseDetailSerializer(serializers.ModelSerializer):
    modules_count = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "slug",
            "title",
            "description",
            "cover_image",
            "is_published",
            "modules_count",
            "lessons_count",
        )

    def get_modules_count(self, obj):
        return obj.modules.count()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(module__course=obj).count()


class LessonTreeSerializer(serializers.ModelSerializer):
    lesson_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ("id", "title", "order", "duration_minutes", "lesson_completed")

    def get_lesson_completed(self, obj):
        completion = self.context.get("completion_map", {})
        return completion.get(obj.id, False)


class ModuleTreeSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ("id", "title", "order", "description", "lessons")

    def get_lessons(self, obj):
        completion_map = self.context.get("completion_map", {})
        return LessonTreeSerializer(
            obj.lessons.all().order_by("order", "id"),
            many=True,
            context={"completion_map": completion_map},
        ).data


class ProblemPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ("id", "order", "prompt", "explanation", "points")


class LessonDetailSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(source="module.id", read_only=True)
    course_id = serializers.IntegerField(source="module.course.id", read_only=True)
    problems = ProblemPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "module_id",
            "course_id",
            "title",
            "order",
            "video_url",
            "content",
            "duration_minutes",
            "problems",
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ("id", "course", "progress_percent", "created_at")


class EnrollResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("id", "user", "course", "progress_percent", "created_at")


class AttemptSubmitSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    answer = serializers.CharField(max_length=255)


class AttemptResultSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    is_correct = serializers.BooleanField()
    awarded_points = serializers.IntegerField()
    lesson_progress = serializers.IntegerField()
    course_progress = serializers.IntegerField()
    correct_answer_if_wrong = serializers.CharField(allow_null=True)


class CourseTreeSerializer(serializers.Serializer):
    course = CourseDetailSerializer()
    modules = serializers.SerializerMethodField()
    course_progress = serializers.IntegerField()

    def get_modules(self, obj):
        request = self.context.get("request")
        completion = lesson_completion_map(obj, request.user if request else None)
        modules = obj.modules.prefetch_related("lessons").all().order_by("order", "id")
        return ModuleTreeSerializer(modules, many=True, context={"completion_map": completion}).data
