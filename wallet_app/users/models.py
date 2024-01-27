from django.core.validators import validate_email
from django.db import models
from django.contrib.auth import models as auth_models
from django.core import validators
from django.urls import reverse


def validate_only_alphabetical(value):
    if not value.isalpha():
        raise validators.ValidationError("Only alphabetical characters are allowed")


class User(auth_models.AbstractUser):
    username = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
        validators=[validate_email],

    )