from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from utils.custom_permissions import CustomPermission
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
# from utils.logger import logger

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
        {"token": token.key, "username": user.username, "admin": user.is_staff},
        status=status.HTTP_200_OK,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "password")

@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
    DEFAULTS = {
        # you can define any defaults that you would like for the user, here
    }
    if User.objects.filter(username=request.data["username"]).exists():
        return Response(
            {
                "detail": "Username already exists",
                "error": "username",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user_data = {
            field: data
            for (field, data) in request.data.items()
            if field in VALID_USER_FIELDS
        }
        user_data.update(DEFAULTS)

        user = get_user_model().objects.create_user(**user_data)

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": UserSerializer(instance=user).data["username"],
                "admin": user.is_staff,
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)