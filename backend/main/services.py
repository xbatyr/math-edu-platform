from django.db.models import Count, Q

from .models import Attempt, Course, Enrollment, Lesson, Problem


def normalize_answer(value):
    return str(value).strip().lower().replace(",", ".")


def grade_attempt(user, problem: Problem, answer: str) -> Attempt:
    normalized_submitted = normalize_answer(answer)
    normalized_correct = normalize_answer(problem.correct_answer)
    is_correct = normalized_submitted == normalized_correct
    awarded_points = problem.points if is_correct else 0

    return Attempt.objects.create(
        user=user,
        problem=problem,
        submitted_answer=str(answer).strip(),
        is_correct=is_correct,
        awarded_points=awarded_points,
    )


def compute_lesson_completion(user, lesson: Lesson) -> bool:
    total = lesson.problems.count()
    if total == 0:
        return False

    solved = (
        Attempt.objects.filter(user=user, problem__lesson=lesson, is_correct=True)
        .values("problem_id")
        .distinct()
        .count()
    )
    return solved >= total


def compute_course_progress(user, course: Course) -> int:
    lessons = Lesson.objects.filter(module__course=course).only("id")
    total_lessons = lessons.count()
    if total_lessons == 0:
        return 0

    completed = sum(1 for lesson in lessons if compute_lesson_completion(user, lesson))
    return int((completed / total_lessons) * 100)


def lesson_completion_map(course: Course, user=None):
    lesson_ids = list(Lesson.objects.filter(module__course=course).values_list("id", flat=True))
    completion = {lesson_id: False for lesson_id in lesson_ids}

    if not user or not user.is_authenticated or not lesson_ids:
        return completion

    solved_counts = (
        Attempt.objects.filter(user=user, problem__lesson_id__in=lesson_ids, is_correct=True)
        .values("problem__lesson_id")
        .annotate(solved=Count("problem", distinct=True))
    )
    total_counts = (
        Problem.objects.filter(lesson_id__in=lesson_ids)
        .values("lesson_id")
        .annotate(total=Count("id"))
    )

    solved_map = {row["problem__lesson_id"]: row["solved"] for row in solved_counts}
    total_map = {row["lesson_id"]: row["total"] for row in total_counts}

    for lesson_id in lesson_ids:
        total = total_map.get(lesson_id, 0)
        completion[lesson_id] = total > 0 and solved_map.get(lesson_id, 0) >= total

    return completion


def upsert_enrollment_progress(user, course: Course) -> Enrollment:
    progress = compute_course_progress(user, course)
    enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)
    if enrollment.progress_percent != progress:
        enrollment.progress_percent = progress
        enrollment.save(update_fields=["progress_percent"])
    return enrollment
