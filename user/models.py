from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(models.Model):

#     GENERIC = 0
#     INSTRUCTOR = 1
#     ADMIN = 2
#     USER_TYPE = ((GENERIC, "GENERIC"), (INSTRUCTOR, "INSTRUCTOR"), (ADMIN, "ADMIN"))

#     email = models.EmailField()
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     role = models.IntegerField(choices=USER_TYPE, default=GENERIC, null=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.first_name + ' ' + self.last_name    
