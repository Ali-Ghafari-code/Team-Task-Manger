from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email_active_code = models.CharField(max_length=100, verbose_name='active code')
