from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from usuario.models import Usuario
from amistad.models import Amistad
from .serializers import *
from rest_framework import permissions
from .permissions import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user.id
        usuario = Usuario.objects.get(user__id=token.user.id)
        return Response({'token': token.key, 'user': user,'usuario': usuario.id})


class UsuarioMixin(object):
  queryset = Usuario.objects.all()
  serializer_class = UsuarioSerializer

"""
class UsuarioList(UsuarioMixin, ListAPIView):
    permission_classes = (permissions.IsAuthenticated,
                  IsAdminOrReadOnly,)
    pass
"""

class UsuarioDetail(UsuarioMixin, RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,
                  IsUsuarioOrReadOnly,)
    pass


class UserMixin(object):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserList(UserMixin, CreateAPIView):
    pass

class UserDetail(UserMixin, RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,
                      IsUserOrReadOnly,)
    pass

class GrupoMixin(object):
    #queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('nombre','ciudad', 'actividades')

    def get_queryset(self, *args, **kwargs):
        queryset_list = Grupo.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(nombre__icontains=query)|
                Q(ciudad__icontains=query)|
                Q(actividades__icontains=query)
                ).distinct()
        return queryset_list

class GrupoList(GrupoMixin, ListCreateAPIView):
    pass

class GrupoDetail(GrupoMixin, RetrieveUpdateAPIView):
    permision_classes = (permissions.IsAuthenticated,)
    pass

class GrupoUsuarioMixin(object):
    serializer_class = GrupoSerializer

    def get_queryset(self):
        user = self.request.user
        usuario = Usuario.objects.get(user=user)
        grupos = Grupo.objects.filter(usuario=usuario)

        return grupos

class GrupoUsuarioList(GrupoUsuarioMixin, ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    pass


class AmistadMixin(object):
  serializer_class = SocialSerializer

  def get_queryset(self):
    user = self.request.user
    friends = Amistad.objects.filter(Q(de=user)|Q(para=user), aceptada=True).values_list('de_id', flat=True)
    friends2 = Amistad.objects.filter(Q(de=user)|Q(para=user), aceptada=True).values_list('para_id', flat=True)
    users = User.objects.filter(Q(id__in=friends)|Q(id__in=friends2)).exclude(id=user.id)

    return users

  #def get_queryset(self):
    #user = self.kwargs['pk']
    #return Amistad.objects.filter(Q(de=self.request.user)|Q(para=self.request.user), aceptada=True)
    #return Amistad.objects.all()

class AmistadList(AmistadMixin, ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass


class CrearAmistadMixin(object):
  queryset = Amistad.objects.all()
  serializer_class = CrearAmistadSerializer

class CrearAmistad(CrearAmistadMixin, CreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass


class ModificarAmistadMixin(object):
  queryset = Amistad.objects.all()
  serializer_class = AmistadSerializer

class AmistadDetail(ModificarAmistadMixin, RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                CanAcceptFriend,)
  pass

class EstadoMixin(object):
  queryset = Publicacion.objects.all()
  serializer_class = EstadoPubSerializer

  #def get_queryset(self):

   # return Estado.objects.filter(publicacion__usuario=self.request.user)

  def perform_create(self, serializer):
    serializer.save(usuario=self.request.user)

  def pre_save(self, obj):
    obj.usuario = self.request.user

class EstadoList(EstadoMixin, CreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass

class EstadoDetail(EstadoMixin, RetrieveDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  IsOwnerOrReadOnly,)
  pass


class ModificarEstadoMixin(object):
  queryset = Estado.objects.all()
  serializer_class = EstadoSerializer

class ModificarEstadoDetail(ModificarEstadoMixin, RetrieveUpdateAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  CanModifEstado,)
  pass


class LikeMixin(object):
  serializer_class = LikeSerializer

  def get_queryset(self):

    return Like.objects.filter(usuario=self.request.user)

  def perform_create(self, serializer):
    serializer.save(usuario=self.request.user)

  def pre_save(self, obj):
    obj.usuario = self.request.user


class LikeList(LikeMixin, ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass

class LikeDetail(LikeMixin, RetrieveDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  CanModifLike,)
  pass


class ExperienciaMixin(object):
  queryset = Publicacion.objects.all()
  serializer_class = ExperienciaPubSerializer

  def perform_create(self, serializer):
    serializer.save(usuario=self.request.user)

  def pre_save(self, obj):
    obj.usuario = self.request.user

class ExperienciaList(ExperienciaMixin, CreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass

class ExperienciaDetail(ExperienciaMixin, RetrieveDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  IsOwnerOrReadOnly,)
  pass


class ModificarExperienciaMixin(object):
  queryset = Experiencia.objects.all()
  serializer_class = ExperienciaSerializer

class ModificarExperienciaDetail(ModificarExperienciaMixin, RetrieveUpdateAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  CanModifExperiencia,)
  pass


class RutaMixin(object):
  queryset = Publicacion.objects.all()
  serializer_class = RutaPubSerializer

  def perform_create(self, serializer):
    serializer.save(usuario=self.request.user)

  def pre_save(self, obj):
    obj.usuario = self.request.user

class RutaList(RutaMixin, CreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass

class RutaDetail(RutaMixin, RetrieveDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  IsOwnerOrReadOnly,)
  pass

class ModificarRutaMixin(object):
  queryset = Ruta.objects.all()
  serializer_class = RutaSerializer

class ModificarRutaDetail(ModificarRutaMixin, RetrieveUpdateAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  CanModifRuta,)


class LugarMixin(object):
  queryset = Lugar.objects.all()
  serializer_class = LugarSerializer

class LugarList(LugarMixin, CreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass

class LugarDetail(LugarMixin, RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  CanModifLugar,)
  pass


class ValoracionMixin(object):
  queryset = Valoracion.objects.all()
  serializer_class = ValoracionSerializer

  def perform_create(self, serializer):
    serializer.save(usuario=self.request.user)

  def pre_save(self, obj):
    obj.usuario = self.request.user

class ValoracionList(ValoracionMixin, ListCreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass

class ValoracionDetail(ValoracionMixin, RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  CanModifValoracion,)
  pass


class ComentarioMixin(object):
  queryset = Comentario.objects.all()
  serializer_class = ComentarioSerializer

  def perform_create(self, serializer):
    serializer.save(usuario=self.request.user)

  def pre_save(self, obj):
    obj.usuario = self.request.user

class ComentarioList(ComentarioMixin, CreateAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass

class ComentarioDetail(ComentarioMixin, RetrieveUpdateDestroyAPIView):
  permission_classes = (permissions.IsAuthenticated,
                  CanModifComentario,)
  pass


class SocialMixin(object):
  serializer_class = SocialSerializer

  def get_queryset(self):

    user = self.request.user
    friends = Amistad.objects.filter(Q(de=user)|Q(para=user), aceptada=True).values_list('de_id', flat=True)
    friends2 = Amistad.objects.filter(Q(de=user)|Q(para=user), aceptada=True).values_list('para_id', flat=True)
    users = User.objects.all().exclude(id__in=friends).exclude(id__in=friends2)

    return users

class SocialList(SocialMixin, ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  pass