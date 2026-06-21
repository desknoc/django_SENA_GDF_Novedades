from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Comunicado
from usuarios.models import Usuario
import base64 #esto es para poder convertir la imagen que nos den el el formulario a base64
# Create your views here.

def Home(request):
    return HttpResponse("Novedades")

def CrearNovedad(request):
    if request.method == 'POST':
        #verificamos que los datos se hayan mandado por POST
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        categoria = request.POST.get('categoria')
        imagen = request.FILES.get('imagen')
        url_referencia = request.POST.get('url_referencia')
        # Verificamos si el usuario esté autenticado y sea admin
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Credenciales inválidas no puede crear novedades'})
        if request.user.rol != 'ADMIN':
            return JsonResponse({'error': 'Solo los admin pueden crear novedades'})
        # Convertimos la imagen que nos mandan del formulario en base64
        if imagen:
            bytes_imagen = imagen.read() # Leemos los bytes del archivo
            imagen_base64 = base64.b64encode(bytes_imagen).decode('utf-8') #lo encodiamos en base64
        else:
            imagen_base64 = '' # crea la variable para guardar la imagen codificada fuera del if
        # Creamos el objeto 'novedad' y mandamos a la base de datos la novedad
        novedad = Comunicado.objects.create(
            titulo = titulo,
            contenido = contenido,
            categoria = categoria,
            imagen_url = imagen_base64,
            url_referencia = url_referencia
        )
        return JsonResponse({'mensaje': 'Novedad creada exitosamente'})
    
    return HttpResponse("Crea Novedades Aquí")

def GestionarNovedad(request):
    return HttpResponse("Gestiona Novedades Aquí")