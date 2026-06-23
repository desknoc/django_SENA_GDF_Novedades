from django.shortcuts import render, get_object_or_404, redirect # El get_object_or_404 es para que si no obtenemos el id nos lance un 404
from django.http import HttpResponse, JsonResponse
from django.db import OperationalError
from .models import Comunicado
from usuarios.models import Usuario
import base64 #esto es para poder convertir la imagen que nos den el el formulario a base64
# Create your views here.

def validar_magic_bytes(bytes_imagen):
    #Verifica que los bytes correspondan a una imagen válida y no monten archivos que no sean una imágen
    #Esta implementación de seguridad me lo dió la IA
    magic_bytes = bytes_imagen[:8]
    
    # JPEG: empieza con FF D8 FF
    if magic_bytes[:3] == b'\xff\xd8\xff':
        return True
    # PNG: empieza con 89 50 4E 47
    if magic_bytes[:4] == b'\x89PNG':
        return True
    # GIF: empieza con 47 49 46
    if magic_bytes[:3] == b'GIF':
        return True
    # WebP: empieza con RIFF y en byte 8 tiene WEBP
    if magic_bytes[:4] == b'RIFF' and bytes_imagen[8:12] == b'WEBP':
        return True
    
    return False

def Home(request):
    if request.method == 'GET':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            # API call - devuelve JSON (comportamiento original)
            novedades = Comunicado.objects.all().values()
            lista_novedades = list(novedades)
            return JsonResponse(lista_novedades, safe=False)
        else:
            # Navegación directa - redirige al template home
            if not request.user.is_authenticated:
                return redirect('login_template')
            nombre = f"{request.user.primer_nombre} {request.user.primer_apellido}"
            return render(request, 'novedades/home.html', {
                'nombre_usuario': nombre
            })
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
            return JsonResponse({'error': 'Credenciales inválidas'})
        if request.user.rol != 'ADMIN':
            return JsonResponse({'error': 'Solo los admin pueden crear novedades'})
        # Convertimos la imagen que nos mandan del formulario en base64
        if imagen:
            if imagen.size > 5 * 1024 * 1024: # establecemos que la imagen sea como máximo de 5MB
                return JsonResponse({'error' : 'La imagen supera el límite permitido'})
            bytes_imagen = imagen.read() # Leemos los bytes del archivo
            if not validar_magic_bytes(bytes_imagen):
                return JsonResponse({'error': 'El archivo no es una imagen válida. Solo se aceptan JPEG, PNG, GIF y WebP.'})
            imagen_base64 = base64.b64encode(bytes_imagen).decode('utf-8') #lo encodiamos en base64
        else:
            imagen_base64 = '' # crea la variable para guardar la imagen codificada fuera del if
        # Creamos el objeto 'novedad' y mandamos a la base de datos la novedad
        try: #Este try está agregado por la IA, lo que está adentro de este try sí lo hice yo
            # De aquí
            novedad = Comunicado.objects.create(
                titulo = titulo,
                contenido = contenido,
                categoria = categoria,
                imagen_url = imagen_base64,
                url_referencia = url_referencia
                # Hasta aquí hice yo, el resto del try con el except es de la IA
            )
        except OperationalError as e: # esto es para que salga un error si la imagen es muy pesada, LO HIZO LA IA
            if e.args[0] == 1153:
                return JsonResponse({'error': 'La imagen supera el límite permitido.'})
            return JsonResponse({'error': 'Error de base de datos. Intentalo de nuevo.'})
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
            return JsonResponse({'error': 'Credenciales inválidas'})
        if request.user.rol != 'ADMIN':
            return JsonResponse({'error': 'Solo los admin pueden editar novedades'})
        # Buscamos la novedad por id
        novedad = get_object_or_404(Comunicado, id=id)
        # Convertimos la imagen que nos mandan del formulario en base64
        if imagen:
            if imagen.size > 5 * 1024 * 1024: # establecemos que la imagen sea como máximo de 5MB
                return JsonResponse({'error' : 'La imagen supera el límite permitido'})
            bytes_imagen = imagen.read() # Leemos los bytes del archivo
            if not validar_magic_bytes(bytes_imagen):
                return JsonResponse({'error': 'El archivo no es una imagen válida. Solo se aceptan JPEG, PNG, GIF y WebP.'})
            imagen_base64 = base64.b64encode(bytes_imagen).decode('utf-8') #lo encodiamos en base64
        else:
            imagen_base64 = ''
        # Actualizamos la base de datos con los nuevos datos proporcionados por el usuario
        # Lo hacemos filtrando por id, para que no se actualicen todas las novedades omaga
        try: # Try hecho con IA pero lo que está adentro lo hice yo
            # De aquí
            Comunicado.objects.filter(id=id).update(
                titulo = titulo,
                contenido = contenido,
                categoria = categoria,
                imagen_url = imagen_base64,
                url_referencia = url_referencia
                # Hasta aquí es mío, el try y el except es de la IA
            )
        except OperationalError as e: # esto es para que salga un error si la imagen es muy pesada, LO HIZO LA IA
            if e.args[0] == 1153:
                return JsonResponse({'error': 'La imagen supera el límite permitido.'})
            return JsonResponse({'error': 'Error de base de datos. Intentalo de nuevo.'}) #esto es una correción que me dió la IA para que no hubieran errores en subir imagenes que sean más pesadas de lo permitido
        return JsonResponse({'mensaje': 'Novedad actualizada correctamente'})
    return HttpResponse("Editar Novedades")

def EliminarNovedad(request, id):
    if request.method == 'POST':
        # Verificamos que el usuario sí esté autenticado y sea ADMIN
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Credenciales inválidas'})
        if request.user.rol != 'ADMIN':
            return JsonResponse({'error': 'Solo los admin pueden eliminar novedades'})
        # Buscamos la novedad por id
        novedad = get_object_or_404(Comunicado, id=id)
        #eliminamos la novedad ya buscada por id
        novedad.delete()
        return JsonResponse({'mensaje': 'Novedad eliminada'})
    return HttpResponse("Eliminar Novedades")

def DetalleNovedad(request, id):
    if request.method == 'GET':
        # Buscamos la novedad por id
        novedad = get_object_or_404(Comunicado, id=id)
        return JsonResponse({
            'id': novedad.id,
            'titulo': novedad.titulo,
            'contenido': novedad.contenido,
            'categoria': novedad.categoria,
            'imagen_url': novedad.imagen_url,
            'url_referencia': novedad.url_referencia,
            'fecha_publicacion': novedad.fecha_publicacion,
            'ultima_actualizacion': novedad.ultima_actualizacion
        })
    return HttpResponse("Detalles de la novedad")


# ============================================================
# VISTAS DE TEMPLATES (Frontend) - NO MODIFICAR LAS DE ARRIBA
# ============================================================

def home_template(request):
    """Vista que renderiza el template del home con novedades"""
    if not request.user.is_authenticated:
        return redirect('login_template')
    
    nombre = f"{request.user.primer_nombre} {request.user.primer_apellido}"
    return render(request, 'novedades/home.html', {
        'nombre_usuario': nombre
    })


def detalle_template(request, id):
    """Vista que renderiza el template de detalle de novedad"""
    if not request.user.is_authenticated:
        return redirect('login_template')
    
    # Verificamos que la novedad exista
    try:
        novedad = Comunicado.objects.get(id=id)
    except Comunicado.DoesNotExist:
        return redirect('error404')
    
    nombre = f"{request.user.primer_nombre} {request.user.primer_apellido}"
    return render(request, 'novedades/detalle.html', {
        'nombre_usuario': nombre,
        'novedad_id': novedad.id
    })


def admin_novedades_template(request):
    """Vista que renderiza el listado admin de novedades"""
    if not request.user.is_authenticated:
        return redirect('login_template')
    if request.user.rol != 'ADMIN':
        return redirect('home')
    
    nombre = f"{request.user.primer_nombre} {request.user.primer_apellido}"
    return render(request, 'novedades/admin/lista.html', {
        'nombre_usuario': nombre
    })


def admin_novedad_crear_template(request):
    """Vista que renderiza el formulario para crear novedad"""
    if not request.user.is_authenticated:
        return redirect('login_template')
    if request.user.rol != 'ADMIN':
        return redirect('home')
    
    nombre = f"{request.user.primer_nombre} {request.user.primer_apellido}"
    return render(request, 'novedades/admin/form.html', {
        'nombre_usuario': nombre,
        'accion': 'crear'
    })


def admin_novedad_editar_template(request, id):
    """Vista que renderiza el formulario para editar novedad"""
    if not request.user.is_authenticated:
        return redirect('login_template')
    if request.user.rol != 'ADMIN':
        return redirect('home')
    
    try:
        novedad = Comunicado.objects.get(id=id)
    except Comunicado.DoesNotExist:
        return redirect('admin_novedades')
    
    nombre = f"{request.user.primer_nombre} {request.user.primer_apellido}"
    return render(request, 'novedades/admin/form.html', {
        'nombre_usuario': nombre,
        'accion': 'editar',
        'novedad_id': novedad.id
    })


def error404_template(request):
    """Vista para páginas no encontradas"""
    return render(request, 'error404.html')