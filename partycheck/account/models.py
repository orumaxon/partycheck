from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email'), blank=True, null=True)
    patronymic = models.CharField(_('patronymic'), max_length=150, blank=True)

    REQUIRED_FIELDS = []
