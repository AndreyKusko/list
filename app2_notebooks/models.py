from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Q

from app1_accounts.models import Library


class NotebookManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | Q(id=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Notebook(models.Model):
    class Meta:
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

    def __str__(self):
        return self.title

    @property
    def tags_indexing(self):
        """
        Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [tag.title for tag in self.tags.all()]


class NoteManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) | Q(id=query)
            )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Note(models.Model):

    class Meta:
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


class Point(models.Model):
    class Meta:
        verbose_name_plural = '1.1.2 Point'
        verbose_name = 'Point'
        ordering = ["user_id", "note", "is_crossed", "ordering_number", "title", "id"]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,)
    note = models.ForeignKey(Note, null=True, on_delete=models.SET_NULL)
    ordering_number = models.IntegerField(verbose_name="Номер", null=True, blank=True)
    title = models.CharField(max_length=120, verbose_name="Название", null=True, blank=True)

    parent_point = models.ForeignKey('Point', blank=True, null=True, on_delete=models.CASCADE, related_name='sub_points')

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
