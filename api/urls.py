from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^users/$', views.UserList.as_view(), name="user_list"),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name="user_detail"),
	url(r'^social/$', views.SocialList.as_view(), name="users_list"),
	url(r'^amistad/$', views.AmistadList.as_view(), name="user_friends"),
	url(r'^amistad/(?P<pk>[0-9]+)/$', views.AmistadDetail.as_view(), name="friendship"),
	url(r'^mis-grupos/$', views.GrupoUsuarioList.as_view(), name="user_groups"),
	url(r'^grupos/$', views.GrupoList.as_view(), name="groups"),
	url(r'^grupos/(?P<pk>[0-9]+)/$', views.GrupoDetail.as_view(), name="group"),
	url(r'^crear-amistad/', views.CrearAmistad.as_view(), name="create_friendship"),
	#url(r'^usuarios/$', views.UsuarioList.as_view(), name="usuario_list"),
	url(r'^usuario/(?P<pk>[0-9]+)/$', views.UsuarioDetail.as_view(), name="user_detail"),
	url(r'^estado/$', views.EstadoList.as_view(), name="estado_list"),
	url(r'^estado/(?P<pk>[0-9]+)/$', views.EstadoDetail.as_view(), name="estado_detail"),
	url(r'^modif-estado/(?P<pk>[0-9]+)/$', views.ModificarEstadoDetail.as_view(), name="modif_estado_detail"),
	url(r'^experiencia/$', views.ExperienciaList.as_view(), name="experiencia_list"),
	url(r'^experiencia/(?P<pk>[0-9]+)/$', views.ExperienciaDetail.as_view(), name="experiencia_detail"),
	url(r'^modif-experiencia/(?P<pk>[0-9]+)/$', views.ModificarExperienciaDetail.as_view(), name="modif_experiencia_detail"),
	url(r'^ruta/$', views.RutaList.as_view(), name="ruta_list"),
	url(r'^ruta/(?P<pk>[0-9]+)/$', views.RutaDetail.as_view(), name="ruta_detail"),
	url(r'^modif-ruta/(?P<pk>[0-9]+)/$', views.ModificarRutaDetail.as_view(), name="modif_ruta_detail"),
	url(r'^lugar/$', views.LugarList.as_view(), name="lugar_list"),
	url(r'^lugar/(?P<pk>[0-9]+)/$', views.LugarDetail.as_view(), name="lugar_detail"),
	url(r'^valoracion/$', views.ValoracionList.as_view(), name="valoracion_list"),
	url(r'^valoracion/(?P<pk>[0-9]+)/$', views.ValoracionDetail.as_view(), name="valoracion_detail"),
	url(r'^comentario/$', views.ComentarioList.as_view(), name="comentario_list"),
	url(r'^comentario/(?P<pk>[0-9]+)/$', views.ComentarioDetail.as_view(), name="comentario_detail"),
	url(r'^likes/$', views.LikeList.as_view(), name="like_list"),
	url(r'^likes/(?P<pk>[0-9]+)/$', views.LikeDetail.as_view(), name="like_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)