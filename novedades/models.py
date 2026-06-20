from django.db import models

# Create your models here.

class comunicados(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.CharField(max_length=1000)
    categoria = models.CharField(max_length=50)
    imagen_url = models.CharField(max_length=500)
    url_referencia = models.CharField(max_length=500)
    fecha_publicacion = models.DateField(auto_now_add=True)
    ultima_actualizacion = models.DateField(auto_now=True)