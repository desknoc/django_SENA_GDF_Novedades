from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.

class AdminUser(UserAdmin):
    list_display = ('primer_nombre', 'primer_apellido', 'tipo_documento', 'documento', 'rol', 'correo_electronico')

    fieldsets = ('INFO_PERSONAL',{'fields':('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tipo_documento', 'documento', 'celular', 'grupo_formacion', 'tipo_apoyo')}), ('INFO_ACCESO',{'fields':('correo_electronico', 'password')}), ('PERMISOS',{'fields':('rol','is_active','is_staff','is_superuser','groups','user_permissions')})

    add_fieldsets = ('ADD_USER',{'fields':('primer_nombre', 'primer_apellido', 'tipo_documento', 'documento', 'celular', 'rol', 'correo_electronico','password1','password2')})

    ordering = ('documento',)

    search_fields = ('documento', 'primer_nombre', 'primer_apellido', 'correo_electronico')

admin.site.register(Usuario, AdminUser)