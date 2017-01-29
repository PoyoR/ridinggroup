from rest_framework import permissions
from publicaciones.models import *
#SAFE_METHODS = ['GET']

class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False

class IsUserOrReadOnly(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return request.user == obj

class IsUsuarioOrReadOnly(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.usuario == request.user

class CanModifEstado(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):

        estado = Estado.objects.get(publicacion=obj.publicacion)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif estado.publicacion.usuario == request.user:
            return True
        else:
            return False

class CanModifExperiencia(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):

        experiencia = Experiencia.objects.get(publicacion=obj.publicacion)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif experiencia.publicacion.usuario == request.user:
            return True
        else:
            return False

class CanModifRuta(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):

        ruta = Ruta.objects.get(publicacion=obj.publicacion)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif ruta.publicacion.usuario == request.user:
            return True
        else:
            return False

class CanModifLugar(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):

        lugar = Lugar.objects.get(ruta=obj.ruta)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif lugar.ruta.publicacion.usuario == request.user:
            return True
        else:
            return False

class CanModifValoracion(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):

        val = Valoracion.objects.get(lugar=obj.ruta)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif val.usuario == request.user:
            return True
        else:
            return False

class CanAcceptFriend(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if not obj.aceptada and obj.para == request.user:
            return True
        elif obj.aceptada and (obj.de == request.user or obj.para == request.user):
            return True
        else:
            return False


class CanModifLike(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):

        like = Like.objects.get(publicacion=obj.publicacion)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif like.usuario == request.user:
            return True
        else:
            return False


class CanModifComentario(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):

        comentario = Comentario.objects.get(publicacion=obj.publicacion)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif comentario.usuario == request.user:
            return True
        else:
            return False