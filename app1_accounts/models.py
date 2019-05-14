# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model


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
        """
        Creates and saves a User with the given username, email and password.
        """
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
    # now that we've abstracted this class we can add any
    # number of custom attribute to our user class
    # in later units we'll be adding things like payment details!
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


class LibraryAccess(models.Model):

    # owner
    # can edit
    # can read
    # blocked

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Users")
    library = models.ForeignKey('Library', on_delete=models.CASCADE,)

    code = models.CharField(max_length=100, null=True, blank=True, verbose_name="Code")
    access_lvl = models.IntegerField(null=True, blank=True, default='0')

    class Meta:
        db_table = 'access_lvl'
        verbose_name_plural = '1.2.2 LibraryAccess'
        verbose_name = 'library access'


class SecretCode(models.Model):
    class Meta:
        db_table = 'secret_code'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    code = models.CharField(max_length=16)


def upload_agreement_location(agreement, filename):
    return "%s/%s" % (agreement, filename)


class Agreement(models.Model):
    class Meta:
        db_table = 'agreement'
        verbose_name_plural = '2.1 Agreement'
        verbose_name = 'agreement'
    pdf = models.FileField(upload_to=upload_agreement_location, null=True, blank=True,)
    text = models.TextField(verbose_name="Text", null=True, blank=True,)
    date = models.TextField(max_length=100, verbose_name="Date")

    def __unicode__(self):
        return self.date


class UserAgree(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    agree = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_agree'
        verbose_name_plural = '2.2 UserAgree'
        verbose_name = 'user_agree'
