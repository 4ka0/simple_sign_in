from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    position = models.CharField(max_length=150, null=True, blank=False)
