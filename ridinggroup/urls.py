from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^token-auth/$', views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
