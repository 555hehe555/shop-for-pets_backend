from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField("email", blank=True, max_length=254)
    description = models.TextField("опис користувача", null=True, max_length=500)

