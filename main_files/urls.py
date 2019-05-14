from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_jwt.views import obtain_jwt_token

from app1_accounts.views import LibraryApiView, UserAPIView
from app2_notebooks.views import *

from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'points', PointApiView)
router.register(r'notebooks', NotebookApiView)
router.register(r'notes', NoteApiView)

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # url(r'^auth/token/api/', obtain_jwt_token),
    url(r'^api/user/$', UserAPIView.as_view(), name='api_user'),

    url(r'^api/library/',           LibraryApiView.as_view(), name='api_libraries'),
    # url(r'^api/notebooks/',         NotebookApiView.as_view(), name='api_notebooks'),

    url(r'^notebook/(?P<notebook_id>\d+)/$', notebook, name='notebook'),
    url(r'^api/', include((router.urls, 'app_name'), namespace='instance_name')),

    url(r'^$', home, name='home'),
]

# urlpatterns += router.urls
urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
