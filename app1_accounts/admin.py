from django.contrib import admin

from app1_accounts import models as app1_models

admin.site.register(app1_models.User)

admin.site.register(app1_models.Library)
