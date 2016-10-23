from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from usuario.models import Usuario

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    #verbose_name_plural = 'Usuarios'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UsuarioInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)