from django.urls import path

from .views import (
    AttemptSubmitView,
    CourseDetailView,
    CourseListView,
    CourseTreeView,
    EnrollView,
    HealthView,
    LessonDetailView,
    LoginView,
    MeView,
    MeEnrollmentsView,
    RefreshView,
    RegisterView,
)

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("courses/", CourseListView.as_view(), name="courses-list"),
    path("courses/<str:course_ref>/", CourseDetailView.as_view(), name="courses-detail"),
    path("courses/<int:course_id>/enroll/", EnrollView.as_view(), name="courses-enroll"),
    path("courses/<int:course_id>/tree/", CourseTreeView.as_view(), name="courses-tree"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lessons-detail"),
    path("attempts/submit/", AttemptSubmitView.as_view(), name="attempt-submit"),
    path("me/enrollments/", MeEnrollmentsView.as_view(), name="me-enrollments"),
]
