from django.contrib import admin
from .models import *

admin.site.register(User)

admin.site.register(Library)

admin.site.register(LibraryAccess)

admin.site.register(UserAgree)

admin.site.register(Agreement)
