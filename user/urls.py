from django.urls import path
from user.views import *

urlpatterns = [
    path("courses", ListCreateCourse.as_view(), name="courses"),
    path("course/<int:pk>", RetrieveUpdateDestroyCourse.as_view(), name="course"),
    path("quizzes", ListCreateQuiz.as_view(), name="quizzes"),
    path("quiz/<int:pk>", RetrieveUpdateDestroyQuiz.as_view(), name="quiz"),
    path("questions", ListCreateQuestion.as_view(), name="questions"),
    path("question/<int:pk>", RetrieveUpdateDestroyQuestion.as_view(), name="question"),
    path("attempts", ListCreateUserAttempt.as_view(), name="attempts"),
]
