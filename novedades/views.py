from django.shortcuts import render, get_object_or_404 # El get_object_or_404 es para que si no obtenemos el id nos lance un 404
from django.http import HttpResponse, JsonResponse
from .models import Comunicado
from usuarios.models import Usuario
import base64 #esto es para poder convertir la imagen que nos den el el formulario a base64
# Create your views here.

def Home(request):
    if request.method == 'GET':
        #Traemos todas las novedades
        novedades = Comunicado.objects.all().values()
        # convertimos las novedades en lista
        lista_novedades = list(novedades)
        return JsonResponse(lista_novedades, safe=False) # Se usa safe=False para que nos acepte lista de datos, ya que solo se aceptan diccionarios por defecto con JsonResponse
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

def EditarNovedad(request, id):
    if request.method == 'POST':
        # Verificamos que recibimos los datos en POST
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        categoria = request.POST.get('categoria')
        imagen = request.FILES.get('imagen')
        url_referencia = request.POST.get('url_referencia')
        # Verificamos que el usuario sí esté autenticado y sea ADMIN
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Credenciales inválidas no puede crear novedades'})
        if request.user.rol != 'ADMIN':
            return JsonResponse({'error': 'Solo los admin pueden editar novedades'})
        # Buscamos la novedad por id
        novedad = get_object_or_404(Comunicado, id=id)
        # Convertimos la imagen que nos mandan del formulario en base64
        if imagen:
            bytes_imagen = imagen.read() # Leemos los bytes del archivo
            imagen_base64 = base64.b64encode(bytes_imagen).decode('utf-8') #lo encodiamos en base64
        else:
            imagen_base64 = ''
        # Actualizamos la base de datos con los nuevos datos proporcionados por el usuario
        # Lo hacemos filtrando por id, para que no se actualicen todas las novedades omaga
        editar = Comunicado.objects.filter(id=id).update(
            titulo = titulo,
            contenido = contenido,
            categoria = categoria,
            imagen_url = imagen_base64,
            url_referencia = url_referencia
        )
        return JsonResponse({'mensaje': 'Novedad actualizada correctamente'})
    return HttpResponse("Editar Novedades")

def EliminarNovedad(request, id):
    if request.method == 'POST':
        # Verificamos que el usuario sí esté autenticado y sea ADMIN
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Credenciales inválidas no puede crear novedades'})
        if request.user.rol != 'ADMIN':
            return JsonResponse({'error': 'Solo los admin pueden eliminar novedades'})
        # Buscamos la novedad por id
        novedad = get_object_or_404(Comunicado, id=id)
        #eliminamos la novedad ya buscada por id
        novedad.delete()
        return JsonResponse({'mensaje': 'Novedad eliminada'})
    return HttpResponse("Eliminar Novedades")