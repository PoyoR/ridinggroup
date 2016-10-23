from django.shortcuts import render
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from usuario.models import Usuario
from .serializers import *
from rest_framework import permissions
from .permissions import IsAdminOrReadOnly, IsUserOrReadOnly


class UsuarioMixin(object):
	queryset = Usuario.objects.all()
	serializer_class = UsuarioSerializer	
	

class UsuarioList(UsuarioMixin, ListAPIView):    
    permission_classes = (permissions.IsAuthenticated,
                  IsAdminOrReadOnly,)
    pass

class UsuarioDetail(UsuarioMixin, RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,
                  IsUserOrReadOnly,)
    pass


class UserMixin(object):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	

class UserList(UserMixin, ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,
                IsAdminOrReadOnly,)
    pass

class UserDetail(UserMixin, RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,
    			IsAdminOrReadOnly,)
    pass