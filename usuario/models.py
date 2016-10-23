from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered

class Usuario(models.Model):    
    user = models.OneToOneField(User)
    edad = models.CharField(max_length=5, blank=True)
    #estado = models.ForeignKey(Estado)
    #municipio = models.ForeignKey(Municipio)
    foto = models.ImageField(upload_to='perfiles', blank=True)
    pro = models.BooleanField(default=False)
    intereses = models.TextField(blank=True)

    def __unicode__(self):
		return self.user.username

"""
def user_registered_callback(sender, user, request, **kwargs):        
    profile = Usuario(user = user)    
    profile.foto = Estado.objects.get(pk=request.POST["estado"])
    profile.municipio = Municipio.objects.get(pk=request.POST["municipio"])    
    profile.save()
 
user_registered.connect(user_registered_callback)
"""