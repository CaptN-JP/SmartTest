from rest_framework import generics
from user.models import (
    Course,
    Quiz,
    User,
    Question,
)
from user.serializers import (
    CourseSerializer,
    QuizSerializer,
    QuestionSerializer,
    UserAttemptSerializer
)
from user import db_queries
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000


class ListCreateCourse(generics.ListCreateAPIView):
    """Create and list courses"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        if self.request.user.role == User.ADMIN:
            user = User.objects.filter(id=self.request.data["creator"]).first()
            if user:
                serializer.save(creator=user)
            else:
                NotFound()
        else:
            raise PermissionDenied()


class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete courses."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def perform_update(self, serializer):
        if self.request.user.role == User.ADMIN:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        if self.request.user.role == User.ADMIN:
            instance.delete()
        else:
            raise PermissionDenied()


class ListCreateQuiz(generics.ListCreateAPIView):
    """Create and list quizzes"""
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        if self.request.user.role == User.INSTRUCTOR:
            serializer.save()
        else:
            raise PermissionDenied()


class RetrieveUpdateDestroyQuiz(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete quizzes."""
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = StandardResultsSetPagination

    def perform_update(self, serializer):
        if self.request.user.role == User.INSTRUCTOR:
            serializer.save()
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        if self.request.user.role == User.INSTRUCTOR:
            instance.delete()
        else:
            raise PermissionDenied()


class ListCreateQuestion(generics.ListCreateAPIView):
    """Create and list questions."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        if self.request.user.role == User.INSTRUCTOR:
            serializer.save()
        else:
            raise PermissionDenied()


class RetrieveUpdateDestroyQuestion(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete questions."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = StandardResultsSetPagination

    def perform_update(self, serializer):
        if self.request.user.role == User.INSTRUCTOR:
            serializer.save()
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        if self.request.user.role == User.INSTRUCTOR:
            instance.delete()
        else:
            raise PermissionDenied()


class ListCreateUserAttempt(generics.ListCreateAPIView):
    """Create and list user attempts."""
    serializer_class = UserAttemptSerializer
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        quiz = self.request.query_params.get("quiz", None)
        return db_queries.get_user_attempts(user, quiz)

    def perform_create(self, serializer):
        if self.request.user.role == User.GENERIC:
            question = Question.objects.filter(id=self.request.data["question"]).first()
            is_right = True if question.answer == self.request.data["selected_option"] else False
            serializer.save(user=self.request.user, is_right=is_right)
        else:
            raise PermissionDenied()
