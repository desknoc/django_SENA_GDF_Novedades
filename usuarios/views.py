from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Usuario

# Create your views here.

def iniciarSesion(request):
    if request.method == 'POST':
        #autenticamos el usuario en la bd
        autenticacion = authenticate(documento = request.POST.get('documento'), password = request.POST.get('password'))
        if autenticacion is not None:
            #Hacemos el login
            login(request, autenticacion)
            return HttpResponse("Inicio de sesión exitoso")
        return HttpResponse("Credenciales inválidas")
    
    return HttpResponse("Iniciar Sesión")

def registrarse(request):
    if request.method == 'POST':
        #recogemos todos los campos
        documento = request.POST.get('documento')
        password = request.POST.get('password')
        primer_nombre = request.POST.get('primer_nombre')
        segundo_nombre = request.POST.get('segundo_nombre')
        primer_apellido = request.POST.get('primer_apellido')
        segundo_apellido = request.POST.get('segundo_apellido')
        tipo_documento = request.POST.get('tipo_documento')
        celular = request.POST.get('celular')
        grupo_formacion = request.POST.get('grupo_formacion')
        correo_electronico = request.POST.get('correo_electronico')

        #verificamos si el usuario ya existe
        if Usuario.objects.filter(tipo_documento = tipo_documento, documento = documento).exists():
            return HttpResponse("El usuario ya existe")
        #creamos el usuario
        registro = Usuario.objects.create_user(documento = documento, password = password, primer_nombre = primer_nombre, segundo_nombre = segundo_nombre, primer_apellido = primer_apellido, segundo_apellido = segundo_apellido, tipo_documento = tipo_documento, celular = celular, grupo_formacion = grupo_formacion, correo_electronico = correo_electronico, rol = 'APRENDIZ', tipo_apoyo = '')
        login(request, registro)
        return HttpResponse("Usuario registrado exitosamente")
        
    return HttpResponse("Registrarse")

def cerrarSesion(request):
    logout(request)
    return HttpResponse("Sesión Cerrada")