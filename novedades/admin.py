from django.contrib import admin
from .models import Comunicado
# Register your models here.

class ComunicadosAdmin (admin.ModelAdmin):
    list_display = ('titulo','categoria','fecha_publicacion','ultima_actualizacion') #esto nos permite visualizar y ingresar campos en el ORM de djangod

admin.site.register(Comunicado, ComunicadosAdmin)
