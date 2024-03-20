from django.urls import path
from userauth.views import login, register

urlpatterns = [
    path("login", login, name="login_api"),
    path("signup", register, name="sign_api"),
]
