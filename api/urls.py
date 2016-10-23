from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^users/$', views.UserList.as_view(), name="user_list"),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name="user_detail"),
	url(r'^usuarios/$', views.UsuarioList.as_view(), name="usuario_list"),
	url(r'^usuarios/(?P<pk>[0-9]+)/$', views.UsuarioDetail.as_view(), name="usuario_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)