import json
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_default_options_json():
    return json.dumps(
        {
            "1": "Option A",
            "2": "Option B",
            "3": "Option C",
            "4": "Option D",
        }
    )


class Course(models.Model):
    """Stores the courses for the quiz."""
    name = models.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quiz(models.Model):
    """Stores the quiz for the courses."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False)
    max_score = models.FloatField(null=False)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    """Stores the questions for the quiz."""

    max_score = models.FloatField(null=False)
    question = models.TextField()
    answer = models.PositiveSmallIntegerField(null=False)
    options = models.JSONField(default=generate_default_options_json)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class UserAttempt(models.Model):
    """Stores the user attempts for the quiz."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.PositiveSmallIntegerField(null=False)
    is_right = models.BooleanField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserReport(models.Model):
    """Stores the user reports for the quiz."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(null=False)
