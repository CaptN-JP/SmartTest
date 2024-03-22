from user.models import UserAttempt


def get_user_attempts(user, quiz):
    return UserAttempt.objects.filter(user=user, quiz=quiz)
