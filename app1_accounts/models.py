# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.conf import settings


class TimeRememberModel(models.Model):
    """
    Time fields for models
    """
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class HiddenNoteModel(TimeRememberModel):
    """
    Hidden notes for models
    """
    hidden_note = models.TextField(max_length=1000, verbose_name="Hidden note", null=True, blank=True)


class AccountUserManager(UserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,)
        user.set_password(password)
        user.save(using=self._db)


class User(AbstractUser):
    class Meta:
        verbose_name_plural = '1.1 User'
        verbose_name = 'User'

    objects = AccountUserManager()


class Library(HiddenNoteModel):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="User", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name="Title")

    class Meta:
        db_table = 'library'
        verbose_name_plural = '1.2.1 Library'
        verbose_name = 'Library'

    def __str__(self):
        library = 'lid=' + str(self.id)
        return library
