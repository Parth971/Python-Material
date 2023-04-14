from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.manager import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14)
    is_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forget_password = models.CharField(max_length=100, null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []