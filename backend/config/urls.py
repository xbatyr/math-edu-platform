from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from main.models import Progress

@csrf_exempt
def complete_lesson(request, lesson_id):
    # временно хардкодим пользователя student1
    user = User.objects.get(username="student1")
    lesson = Lesson.objects.get(id=lesson_id)

    Progress.objects.update_or_create(
        user=user, lesson=lesson,
        defaults={"completed": True}
    )
    return redirect(f"/lessons/{lesson_id}/")


def hello(request):
    return HttpResponse("""
    <h1>Привет</h1>
    <p>Это моя первая HTML-страница на Django</p>
    """)

from main.models import Course, Lesson

def courses(request):
    qs = Course.objects.all()

    html = "<h1>Курсы (из базы)</h1><ul>"
    for c in qs:
        html += f"<li>{c.id}. {c.title}</li>"
    html += "</ul>"

    return HttpResponse(html)

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = course.lessons.all().order_by("order")

    html = f"<h1>{course.title}</h1><ul>"
    for l in lessons:
        html += f'<li>{l.order}. <a href="/lessons/{l.id}/">{l.title}</a></li>'
    html += "</ul>"
    return HttpResponse(html)

def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    html = f"<h1>{lesson.title}</h1>"

    if lesson.video_url:
        url = lesson.video_url
        video_id = None

        # 1) https://www.youtube.com/watch?v=ID
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]

        # 2) https://youtu.be/ID
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]

        if video_id:
            html += f"""
            <iframe width="560" height="315"
                src="https://www.youtube.com/embed/{video_id}"
                frameborder="0" allowfullscreen>
            </iframe>
            """
        else:
            html += f'<p><a href="{url}">Видео</a></p>'

    if lesson.content_text:
        html += f"<p>{lesson.content_text}</p>"
    html += f"""
<form method="post" action="/lessons/{lesson.id}/complete/">
  <button type="submit">Отметить как пройдено</button>
</form>
"""

    return HttpResponse(html)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello),
    path("courses/", courses),
    path("courses/<int:course_id>/", course_detail),
    path("lessons/<int:lesson_id>/", lesson_detail),
    path("lessons/<int:lesson_id>/complete/", complete_lesson),

]

