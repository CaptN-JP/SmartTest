from django.urls import path
from user.views import login, register

urlpatterns = [
    path("login", login, name="login_api"),
    path("signup", register, name="sign_api"),
]
