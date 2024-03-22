from rest_framework import serializers

from user.models import (
    Course,
    Quiz,
    Question,
    UserAttempt,
    UserReport,
)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class UserAttemptSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttempt
        fields = "__all__"
        # For POST request, if user and quiz are not provided, then it will be taken from the request.
        extra_kwargs = {
            "user": {"required": False},
            "is_right": {"required": False},
        }
