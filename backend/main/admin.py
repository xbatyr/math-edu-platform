from django.contrib import admin

from .models import Attempt, Course, Enrollment, Lesson, Module, Problem


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "order", "created_at")
    list_filter = ("course",)
    ordering = ("course", "order")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "module", "order", "duration_minutes")
    list_filter = ("module__course",)
    ordering = ("module", "order")


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "lesson", "order", "points")
    list_filter = ("lesson__module__course",)
    ordering = ("lesson", "order")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "progress_percent", "created_at")
    list_filter = ("course",)
    search_fields = ("user__username", "course__title")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "problem", "is_correct", "awarded_points", "created_at")
    list_filter = ("is_correct", "problem__lesson__module__course")
    search_fields = ("user__username",)
