from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENERIC = 0
    INSTRUCTOR = 1
    ADMIN = 2
    USER_TYPE = ((GENERIC, "GENERIC"), (INSTRUCTOR, "INSTRUCTOR"), (ADMIN, "ADMIN"))

    role = models.PositiveSmallIntegerField(choices=USER_TYPE, default=GENERIC, null=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
