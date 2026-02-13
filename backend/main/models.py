from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "course"
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["course", "order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_module_order_per_course"),
        ]

    def __str__(self):
        return f"{self.course.title} / {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    video_url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["module", "order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["module", "order"], name="unique_lesson_order_per_module"),
        ]

    def __str__(self):
        return f"{self.module.title} / {self.title}"


class Problem(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="problems")
    order = models.PositiveIntegerField(default=1)
    prompt = models.TextField()
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)
    points = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["lesson", "order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["lesson", "order"], name="unique_problem_order_per_lesson"),
        ]

    def __str__(self):
        return f"Problem {self.id} ({self.lesson.title})"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    progress_percent = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="unique_enrollment_per_user_course"),
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="attempts")
    submitted_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    awarded_points = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "problem", "-created_at"], name="attempt_usr_prob_cr_idx"),
        ]

    def __str__(self):
        return f"{self.user.username} / problem {self.problem_id}"
