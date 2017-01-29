from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from usuario.models import Usuario, Grupo, Pais, Region, Moto
from amistad.models import Amistad
from publicaciones.models import *

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

#Serializar todos los paises
class PaisSerializer(serializers.ModelSerializer):

	class Meta:
		model = Pais
		fields = '__all__'

#Serializar todas las regiones
class RegionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Region
		fields = '__all__'

#Serializar todos los grupos creados por usuarios
class GrupoSerializer(serializers.ModelSerializer):
    miembros = serializers.SerializerMethodField()
    foto = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
		model = Grupo
		fields = '__all__'
		filter_backends = (DjangoFilterBackend,)
		filter_fields = ('nombre',)

    def get_miembros(self,obj):
	    miembros = Usuario.objects.filter(grupo=obj).count()
	    return miembros

#Serializar todas las amistades
class AmistadSerializer(serializers.ModelSerializer):
	de = serializers.CharField(source="de.username")
	para = serializers.CharField(source="para.username")

	class Meta:
		model = Amistad
		fields = '__all__'

#Amistades serializadas para poder crearlas
class CrearAmistadSerializer(serializers.ModelSerializer):

	class Meta:
		model = Amistad
		fields = '__all__'

class MotoSerializer(serializers.ModelSerializer):
    foto = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
        model = Moto
        fields = '__all__'


#Serializar el objeto usuario (datos adicionales)
class UsuarioSerializer(serializers.ModelSerializer):
	#user = serializers.ReadOnlyField()
	pro = serializers.ReadOnlyField()
	grupo = serializers.SlugRelatedField(many=True, queryset=Grupo.objects.all(), slug_field='nombre', required=False)
	nom_pais = serializers.ReadOnlyField(source='pais.nombre')
	nom_region = serializers.ReadOnlyField(source='region.nombre')
	foto = Base64ImageField(max_length=None, use_url=True,)


	class Meta:
		model = Usuario
		fields = ('id', 'edad', 'foto', 'pro', 'intereses', 'ubicacion', 'grupo', 'pais', 'nom_pais', 'region', 'nom_region', 'ciudad')

class UserSerializer2(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username')

#Serializar el objeto user para poder registrar usuarios y obtener sus datos
class UserSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer()
	motos = serializers.SerializerMethodField()
	amistad = serializers.SerializerMethodField()
	estados = serializers.SerializerMethodField()
	experiencias = serializers.SerializerMethodField()
	rutas = serializers.SerializerMethodField()
	password = serializers.CharField(write_only=True, min_length=5)
	email = serializers.EmailField(validators=[UniqueValidator(
		message="Una cuenta con este correo ya se encuentra registrada, por favor elija otra",
		queryset=User.objects.all())])

	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'password', 'email',
			'usuario', 'motos','amistad', 'estados', 'experiencias', 'rutas')

	def get_motos(self,user):
	    moto = Moto.objects.filter(usuario=user)
	    serializer = MotoSerializer(instance=moto, many=True)
	    return serializer.data

	def get_amistad(self, user):
		#user = self.request.user
		friends = Amistad.objects.filter(Q(de=user)|Q(para=user), aceptada=True).values_list('de_id', flat=True)
		friends2 = Amistad.objects.filter(Q(de=user)|Q(para=user), aceptada=True).values_list('para_id', flat=True)
		users = User.objects.filter(Q(id__in=friends)|Q(id__in=friends2)).exclude(id=user.id)
		serializer = UserSerializer2(instance=users, many=True)
		return serializer.data

	def get_estados(self, user):
		estados = Estado.objects.filter(publicacion__usuario=user)
		serializer = EstadoSerializer(instance=estados, many=True)
		return serializer.data

	def get_experiencias(self, user):
		experiencias = Experiencia.objects.filter(publicacion__usuario=user)
		serializer = ExperienciaSerializer(instance=experiencias, many=True)
		return serializer.data

	def get_rutas(self, user):
		rutas = Ruta.objects.filter(publicacion__usuario=user)
		serializer = RutaSerializer(instance=rutas, many=True)
		return serializer.data

	def create(self, validated_data):
		profile_data = validated_data.pop('usuario')
		user = User.objects.create(**validated_data)
		user.set_password(validated_data['password'])
		user.save()
		usuario = Usuario.objects.create(user=user)
		return user

#Serializar likes
class LikeSerializer(serializers.ModelSerializer):
	usuario = serializers.SerializerMethodField()

	class Meta:
		model = Like
		fields = ('id', 'usuario', 'publicacion')

	def get_usuario(self,obj):
		usuario = obj.usuario
		user = get_object_or_404(User, pk=usuario.pk)
		serializer = UserSerializer2(instance=user)
		return serializer.data


class ComentarioSerializer(serializers.ModelSerializer):
	usuario = serializers.SerializerMethodField()

	class Meta:
		model = Comentario
		fields = ('id', 'usuario', 'comentario')

	def get_usuario(self,obj):
		usuario = obj.usuario
		user = get_object_or_404(User, pk=usuario.pk)
		serializer = UserSerializer2(instance=user)
		return serializer.data


#Serializar los estados (para poder ser modificados)
class EstadoSerializer(serializers.ModelSerializer):
	comentarios = serializers.SerializerMethodField()
	total_likes = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()
	imagen = Base64ImageField(max_length=None, use_url=True,)

	class Meta:
		model = Estado
		fields = ('id','texto', 'imagen', 'comentarios','total_likes','likes')

	def get_comentarios(self, obj):
		comentarios = Comentario.objects.filter(publicacion=obj.publicacion)
		serializer = ComentarioSerializer(instance=comentarios, many=True)
		return serializer.data

	def get_total_likes(self, obj):
		total_likes  = Like.objects.filter(publicacion=obj.publicacion).count()
		return total_likes

	def get_likes(self, obj):
		likes = Like.objects.filter(publicacion=obj.publicacion)
		serializer = LikeSerializer(instance=likes, many=True)
		return serializer.data

#serializar las publicaciones + estados
class EstadoPubSerializer(serializers.ModelSerializer):
	estado = EstadoSerializer()
	usuario = serializers.ReadOnlyField(source='usuario.username')

	class Meta:
		model = Publicacion
		fields = ('id', 'usuario', 'fecha', 'estado')

	def create(self, validated_data):
		estado_data = validated_data.pop('estado')
		pub = Publicacion.objects.create(**validated_data)
		estado = Estado.objects.create(publicacion=pub, **estado_data)

		return pub

#Serializar experiencias
class ExperienciaSerializer(serializers.ModelSerializer):
	comentarios = serializers.SerializerMethodField()
	total_likes = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()
	imagen = Base64ImageField(max_length=None, use_url=True,)

	class Meta:
		model = Experiencia
		fields = ('id', 'texto', 'imagen', 'comentarios', 'total_likes', 'likes')

	def get_comentarios(self, obj):
		comentarios = Comentario.objects.filter(publicacion=obj.publicacion)
		serializer = ComentarioSerializer(instance=comentarios, many=True)
		return serializer.data

	def get_total_likes(self, obj):
		total_likes  = Like.objects.filter(publicacion=obj.publicacion).count()
		return total_likes

	def get_likes(self, obj):
		likes = Like.objects.filter(publicacion=obj.publicacion)
		serializer = LikeSerializer(instance=likes, many=True)
		return serializer.data

class ExperienciaPubSerializer(serializers.ModelSerializer):
	experiencia = ExperienciaSerializer()
	usuario = serializers.ReadOnlyField(source='usuario.username')

	class Meta:
		model = Publicacion
		fields = ('id', 'usuario', 'fecha', 'experiencia')

	def create(self, validated_data):
		experiencia_data = validated_data.pop('experiencia')
		pub = Publicacion.objects.create(**validated_data)
		estado = Experiencia.objects.create(publicacion=pub, **experiencia_data)

		return pub


class LugarSerializer(serializers.ModelSerializer):
    imagen = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
		model = Lugar
		fields = ('id', 'ruta', 'nombre', 'coordenadas', 'imagen')


class ValoracionSerializer(serializers.ModelSerializer):
	usuario = serializers.ReadOnlyField(source='usuario.username')

	class Meta:
		model = Valoracion
		fields = ('id', 'ruta', 'usuario', 'calificacion')


class RutaSerializer(serializers.ModelSerializer):
	lugares = serializers.SerializerMethodField()
	valoraciones = serializers.SerializerMethodField()
	comentarios = serializers.SerializerMethodField()
	total_likes = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()

	class Meta:
		model = Ruta
		fields = ('id', 'origen', 'destino', 'pais', 'lugares', 'valoraciones',
			'comentarios','total_likes', 'likes')

	def get_lugares(self, obj):
		lugares = Lugar.objects.filter(ruta=obj)
		serializer = LugarSerializer(instance=lugares, many=True)
		return serializer.data

	def get_valoraciones(self, obj):
		valoraciones = Valoracion.objects.filter(ruta=obj)
		serializer = ValoracionSerializer(instance=valoraciones, many=True)
		return serializer.data

	def get_comentarios(self, obj):
		comentarios = Comentario.objects.filter(publicacion=obj.publicacion)
		serializer = ComentarioSerializer(instance=comentarios, many=True)
		return serializer.data

	def get_total_likes(self, obj):
		total_likes  = Like.objects.filter(publicacion=obj.publicacion).count()
		return total_likes

	def get_likes(self, obj):
		likes = Like.objects.filter(publicacion=obj.publicacion)
		serializer = LikeSerializer(instance=likes, many=True)
		return serializer.data

class RutaPubSerializer(serializers.ModelSerializer):
	ruta = RutaSerializer()
	usuario = serializers.ReadOnlyField(source="usuario.username")

	class Meta:
		model = Publicacion
		fields = ('id', 'usuario', 'fecha', 'ruta')

	def create(self, validated_data):
		ruta_data = validated_data.pop('ruta')
		pub = Publicacion.objects.create(**validated_data)
		estado = Ruta.objects.create(publicacion=pub, **ruta_data)

		return pub


class SocialSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer()
	motos = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'usuario', 'motos')

	def get_motos(self,obj):
	    moto = Moto.objects.filter(usuario=obj.id)
	    serializer = MotoSerializer(instance=moto, many=True)
	    return serializer.data