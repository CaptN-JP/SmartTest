from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from utils.custom_permissions import CustomPermission
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

# from utils.logger import logger

User = get_user_model()
User._meta.get_field("username")._unique = True


@api_view(["POST"])
# @permission_classes((AllowAny, CustomPermission,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {
                "detail": "Please provide both username and password",
                "error": "Blank field",
            },
            status=HTTP_400_BAD_REQUEST,
        )
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {
                "detail": "Invalid Credentials",
                "error": "Invalid Credentials",
            },
            status=HTTP_403_FORBIDDEN,
        )
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"id": user.id, "token": token.key, "username": user.username, "role": user.role},
        status=status.HTTP_200_OK,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "password", "role")
        extra_kwargs = {
            "username": {
                "error_messages": {"required": "Please enter a username."}
            },
            "password": {
                "error_messages": {"required": "Please enter a password."}
            },
        }


@api_view(["POST"])
# @permission_classes((AllowAny,))
def register(request):
    user_data = request.data.copy()
    user_serializer = UserSerializer(data=user_data)

    if user_serializer.is_valid():
        if get_user_model().objects.filter(username=user_data["username"]).exists():
            return Response(
                {"detail": "Username already exists", "error": "username"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = user_serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"id": user.id, "token": token.key, "username": user.username, "role": user.role},
                        status=status.HTTP_201_CREATED,
                        )
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
