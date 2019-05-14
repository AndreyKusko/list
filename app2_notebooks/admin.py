from django.contrib import admin

from .models import *


class NotebookAdmin(admin.ModelAdmin):
    class Meta:
        model = Point
    list_display = ['user', 'library', 'title', 'is_deleted']
    list_display_links = ['title']


admin.site.register(Notebook, NotebookAdmin)


admin.site.register(Note)


class PointAdmin(admin.ModelAdmin):
    class Meta:
        model = Point
    list_display = ['note', 'ordering_number', 'title', 'parent_point']
    list_display_links = ['note', 'ordering_number', 'title']


admin.site.register(Point, PointAdmin)
