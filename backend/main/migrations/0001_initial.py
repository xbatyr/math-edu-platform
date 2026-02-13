# Generated manually for reset-dev schema

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
                ("cover_image", models.URLField(blank=True)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={"ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("order", models.PositiveIntegerField(default=1)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="modules", to="main.course")),
            ],
            options={"ordering": ["course", "order", "id"]},
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("order", models.PositiveIntegerField(default=1)),
                ("video_url", models.URLField(blank=True)),
                ("content", models.TextField(blank=True)),
                ("duration_minutes", models.PositiveIntegerField(default=20)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("module", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lessons", to="main.module")),
            ],
            options={"ordering": ["module", "order", "id"]},
        ),
        migrations.CreateModel(
            name="Problem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=1)),
                ("prompt", models.TextField()),
                ("correct_answer", models.CharField(max_length=255)),
                ("explanation", models.TextField(blank=True)),
                ("points", models.PositiveSmallIntegerField(default=1)),
                ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="problems", to="main.lesson")),
            ],
            options={"ordering": ["lesson", "order", "id"]},
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "progress_percent",
                    models.PositiveSmallIntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)],
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="enrollments", to="main.course")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enrollments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("submitted_answer", models.CharField(max_length=255)),
                ("is_correct", models.BooleanField(default=False)),
                ("awarded_points", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("problem", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attempts", to="main.problem")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attempts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [models.Index(fields=["user", "problem", "-created_at"], name="attempt_usr_prob_cr_idx")],
            },
        ),
        migrations.AddConstraint(
            model_name="module",
            constraint=models.UniqueConstraint(fields=("course", "order"), name="unique_module_order_per_course"),
        ),
        migrations.AddConstraint(
            model_name="lesson",
            constraint=models.UniqueConstraint(fields=("module", "order"), name="unique_lesson_order_per_module"),
        ),
        migrations.AddConstraint(
            model_name="problem",
            constraint=models.UniqueConstraint(fields=("lesson", "order"), name="unique_problem_order_per_lesson"),
        ),
        migrations.AddConstraint(
            model_name="enrollment",
            constraint=models.UniqueConstraint(fields=("user", "course"), name="unique_enrollment_per_user_course"),
        ),
    ]
