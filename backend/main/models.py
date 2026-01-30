from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=1)
    video_url = models.URLField(blank=True)
    content_text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course.title}: {self.title}"

from django.contrib.auth.models import User

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
