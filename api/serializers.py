from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from usuario.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Usuario
		fields = ('id', 'edad')

class UserSerializer(serializers.ModelSerializer):
	#usuario = UsuarioSerializer()
	password = serializers.CharField(write_only=True, min_length=5)
	email = serializers.EmailField(validators=[UniqueValidator(
		message="Una cuenta con este correo ya se encuentra registrada, por favor elija otra",
		queryset=User.objects.all())])

	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'email')

	def create(self, validated_data):
		profile_data = validated_data.pop('usuario')
		user = User.objects.create(**validated_data)
		user.set_password(validated_data['password'])
		user.save()
		Usuario.objects.create(user=user, **profile_data)
		return user