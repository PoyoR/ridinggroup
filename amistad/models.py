from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Amistad(models.Model):
	de = models.ForeignKey('auth.user', related_name='solicitud_enviada')
	para = models.ForeignKey(User, related_name='solicitud_recibida')
	fecha = models.DateField(auto_now_add=True)
	aceptada = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s - %s" % (self.de.username, self.para.username)