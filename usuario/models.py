from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered

class Pais(models.Model):
	nombre = models.CharField(max_length=50)

	def __unicode__(self):
		return self.nombre

class Region(models.Model):
	pais = models.ForeignKey(Pais)
	nombre = models.CharField(max_length=100)

	def __unicode__(self):
		return "%s - %s" % (self.pais, self.nombre)

class Grupo(models.Model):
	creador = models.ForeignKey(User)
	nombre = models.CharField(max_length=80, unique=True)
	pais = models.ForeignKey(Pais)
	actividades = models.TextField()
	foto = models.ImageField(upload_to='fotos grupos', blank=True, null=True)
	region = models.ForeignKey(Region)
	ciudad = models.CharField(max_length=100)

	def __unicode__(self):
		return self.nombre

class Usuario(models.Model):
    user = models.OneToOneField(User)
    edad = models.CharField(max_length=5, blank=True, null=True)
    foto = models.ImageField(upload_to='perfiles', blank=True, null=True)
    pro = models.BooleanField(default=False)
    intereses = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=80, blank=True, null=True)
    grupo = models.ManyToManyField(Grupo, blank=True)
    pais = models.ForeignKey(Pais, blank=True, null=True)
    region = models.ForeignKey(Region, blank=True, null=True)
    ciudad = models.CharField(max_length=100,  blank=True, null=True)

    def __unicode__(self):
		return self.user.username

class Moto(models.Model):
	usuario = models.ForeignKey(User)
	marca = models.CharField(max_length=100)
	modelo = models.CharField(max_length=100)
	foto = models.ImageField(upload_to='motos', blank=True)
	proposito = models.TextField()

	def __unicode__(self):
		return "%s - %s" % (self.marca, self.usuario.user.username)



"""
def user_registered_callback(sender, user, request, **kwargs):
    profile = Usuario(user = user)
    profile.foto = Estado.objects.get(pk=request.POST["estado"])
    profile.municipio = Municipio.objects.get(pk=request.POST["municipio"])
    profile.save()

user_registered.connect(user_registered_callback)
"""