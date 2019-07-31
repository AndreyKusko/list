from django.contrib import admin

from app2_notebooks import models as app2_models


class NotebookAdmin(admin.ModelAdmin):
    class Meta:
        model = app2_models.Point
    list_display = ['user', 'library', 'title', 'is_deleted']
    list_display_links = ['title']


admin.site.register(app2_models.Notebook, NotebookAdmin)


admin.site.register(app2_models.Note)


class PointAdmin(admin.ModelAdmin):
    class Meta:
        model = app2_models.Point
    list_display = ['note', 'ordering_number', 'title', 'parent_point']
    list_display_links = ['note', 'ordering_number', 'title']


admin.site.register(app2_models.Point, PointAdmin)
