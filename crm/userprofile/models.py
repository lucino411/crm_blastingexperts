from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=False)
    is_organizator = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)

