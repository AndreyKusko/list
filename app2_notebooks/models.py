from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from app1_accounts.models import Library

from ckeditor.fields import RichTextField

from django.db import models


# from .search import NotebookIndex
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import Q


class NotebookManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(id=query)
            )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Notebook(models.Model):
    class Meta:
        db_table = 'notebook'
        verbose_name_plural = '1 Notebook'
        verbose_name = 'Notebook'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User", null=True, on_delete=models.SET_NULL)
    library = models.ForeignKey(Library, null=True, on_delete=models.SET_NULL)

    ordering_number = models.IntegerField(verbose_name="_ordering_number", default=0, null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name="Title")

    is_deleted = models.BooleanField(default=False, verbose_name="is_deleted")
    hidden_note = models.TextField(max_length=1000, verbose_name="Hidden note", null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # objects = NotebookManager()

    # def __str__(self):
    #     library = 'lid=' + str(self.library.id) + ' | '
    #     notebook = 'nbid=' + str(self.id) + ' | ' + str(self.title)
    #     return library + notebook
        # return notebook

    def __str__(self):
        return self.title

    @property
    def tags_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [tag.title for tag in self.tags.all()]



# class Paper(models.Model):
#     class Meta:
#         db_table = 'paper'
#         verbose_name_plural = '1.1 Paper'
#         verbose_name = 'Paper'
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,)
#     notebook = models.ForeignKey(Notebook, null=True, on_delete=models.SET_NULL,)
#
#     ordering_number = models.IntegerField(verbose_name="_ordering_number", null=True, blank=True)
#     title = models.CharField(max_length=100, verbose_name="Title", null=True, blank=True)
#
#     note = models.TextField(max_length=3000, verbose_name="Hidden note", null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#     timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class NoteManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(id=query)
            )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Note(models.Model):
    class Meta:
        db_table = 'note'
        verbose_name_plural = '1.1.1 Note'
        verbose_name = 'Note'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,)
    notebook = models.ForeignKey(Notebook, null=True, related_name='note', on_delete=models.SET_NULL,)

    ordering_number = models.IntegerField(verbose_name="_ordering_number", null=True, blank=True)

    is_note = models.BooleanField(default=False, verbose_name="is_note")
    is_list = models.BooleanField(default=False, verbose_name="is_list")

    title = models.CharField(max_length=100, verbose_name="Title", null=True, blank=True)
    # ck_text = RichTextField(max_length=10000, verbose_name="CK Text", null=True, blank=True)
    text = models.TextField(max_length=10000, verbose_name="text without format", null=True, blank=True)

    hidden_note = models.TextField(max_length=3000, verbose_name="Hidden note", null=True, blank=True)

    is_deleted = models.BooleanField(default=False, verbose_name="is_deleted")

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = NoteManager()


# class Clip(models.Model):
#     class Meta:
#         db_table = 'clip'
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,)
#     notebook = models.ForeignKey(NoteBook, null=True, on_delete=models.SET_NULL,)
#     title = models.CharField(max_length=500, verbose_name="Название")
#     number = models.IntegerField(verbose_name="Номер", null=True, blank=True)
#     hidden_note = models.TextField(max_length=3000, verbose_name="Скрытая заметка", null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#     timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
#
#     def __unicode__(self):
#         name = 123
#         return name


class Point(models.Model):
    class Meta:
        db_table = 'point'
        verbose_name_plural = '1.1.2 Point'
        verbose_name = 'Point'
        ordering = ["user_id", "note", "ordering_number", "id", "title"]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,)
    note = models.ForeignKey(Note, null=True, on_delete=models.SET_NULL)
    ordering_number = models.IntegerField(verbose_name="Номер", null=True, blank=True)
    title = models.CharField(max_length=120, verbose_name="Название", null=True, blank=True)

    parent_point = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='sub_points')

    text = models.TextField(default=False, max_length=3000, verbose_name="Текст", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    is_crossed = models.BooleanField(default=False, verbose_name="is_crossed out")

    hidden_note = models.TextField(max_length=3000, verbose_name="Скрытая заметка", null=True, blank=True)

    is_deleted = models.BooleanField(default=False, verbose_name="is_deleted")

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        notebook = 'nbid=' + str(self.id) + ' | ' + str(self.title)
        return notebook


# class PointAddition(models.Model):
#     class Meta:
#         db_table = 'point_addition'
#         ordering = ["timestamp"]
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,)
#     point = models.ForeignKey(Point, null=True, on_delete=models.SET_NULL,)
#     order_number = models.IntegerField(default="0", verbose_name="Номер", null=True, blank=True,)
#
#     title = models.CharField(max_length=120, verbose_name="Название", null=True, blank=True)
#     number = models.IntegerField(verbose_name="Номер", null=True, blank=True)
#     text = models.TextField(default=False, max_length=3000, verbose_name="Текст", null=True, blank=True)
#
#     data_new_point_new_add = models.IntegerField(default="0", verbose_name="Номер", null=True, blank=True)
#     hidden_note = models.TextField(max_length=3000, verbose_name="Скрытая заметка", null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#     timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
#
#     def __unicode__(self):
#         if self.user.every.name:
#             b = 'biz' + ' ' + self.user.every.name
#         else:
#             b = 'person' + ' ' + self.user.every.person_name
#         if self.number:
#             n = str(self.number)
#         else:
#             n = ''
#         if self.title:
#             t = self.title
#         else:
#             t = ''
#         name = b + str(self.user.id) + ' | ' + n + ' | ' + t
#
#         return name