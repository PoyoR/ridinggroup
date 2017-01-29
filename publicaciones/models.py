from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from usuario.models import Pais

class Publicacion(models.Model):
	usuario = models.ForeignKey(User)
	fecha = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return "%s - %s" % (self.pk, self.usuario.username) 

class Estado(models.Model):
	publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE)
	texto = models.TextField()
	imagen = models.ImageField(upload_to='estados', blank=True, null=True)

	def __unicode__(self):
		return "%s %s" % (self.publicacion.pk, self.publicacion.usuario.username)

class Experiencia(models.Model):
	publicacion = models.OneToOneField(Publicacion)
	texto = models.TextField()
	imagen = models.ImageField(upload_to='experiencias', blank=True, null=True)

	def __unicode__(self):
		return self.publicacion.usuario.username

class Ruta(models.Model):
	publicacion = models.OneToOneField(Publicacion)
	texto = models.TextField()
	origen = models.CharField(max_length=50)
	destino = models.CharField(max_length=50)
	pais = models.ForeignKey(Pais)

	def __unicode__(self):
		return self.publicacion.usuario.username

class Lugar(models.Model):
	ruta = models.ForeignKey(Ruta)
	nombre = models.CharField(max_length=100)
	coordenadas = models.CharField(max_length=50)
	imagen = models.ImageField(upload_to='lugares', blank=True, null=True)

	def __unicode__(self):
		return self.nombre

class Recomendacion(models.Model):
	publicacion = models.OneToOneField(Publicacion)
	lugar = models.ForeignKey(Lugar)
	texto = models.TextField()

	def __unicode__(self):
		return self.publicacion.usuario.username

class Valoracion(models.Model):
	ruta = models.ForeignKey(Ruta)
	usuario = models.ForeignKey(User)
	calificacion = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return str(self.calificacion)

class Comentario(models.Model):
	usuario = models.ForeignKey(User)
	publicacion = models.ForeignKey(Publicacion)
	comentario = models.TextField()

	def __unicode__(self):
		return self.usuario.username

class Like(models.Model):
	usuario = models.ForeignKey(User)
	publicacion = models.ForeignKey(Publicacion)

	def __unicode__(self):
		return self.usuario.username