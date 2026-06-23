from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Usuario
from senagdf.validators import validar_documento, validar_nombre, validar_celular, validar_correo

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
    
    # Si alguien accede directamente a /usuarios/ en el navegador
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login_template')

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

        # Validaciones con regex
        errores = [] # Metemos los errores dentro de este array para luego mandar una lista de errores
        if not validar_documento(documento):
            errores.append("El documento debe tener 10 dígitos")
        if not validar_nombre(primer_nombre):
            errores.append("El primer nombre solo puede incluír letras")
        if segundo_nombre and not validar_nombre(segundo_nombre):
            errores.append("El segundo nombre solo puede incluír letras")
        if not validar_nombre(primer_apellido):
            errores.append("El primer apellido solo puede incluír letras")
        if segundo_apellido and not validar_nombre(segundo_apellido):
            errores.append("El segundo apellido solo puede incluír letras")
        if not validar_celular(celular):
            errores.append("El celular debe tener 10 dígitos")
        if not validar_correo(correo_electronico):
            errores.append("El correo electrónico debe estar completo")
        if errores:
            return HttpResponse(" | ".join(errores))

        #verificamos si el usuario ya existe
        if Usuario.objects.filter(tipo_documento = tipo_documento, documento = documento).exists():
            return HttpResponse("El usuario ya existe")
        #creamos el usuario
        registro = Usuario.objects.create_user(documento = documento, password = password, primer_nombre = primer_nombre, segundo_nombre = segundo_nombre, primer_apellido = primer_apellido, segundo_apellido = segundo_apellido, tipo_documento = tipo_documento, celular = celular, grupo_formacion = grupo_formacion, correo_electronico = correo_electronico, rol = 'APRENDIZ', tipo_apoyo = '')
        login(request, registro)
        return HttpResponse("Usuario registrado exitosamente")
    
    # GET request - redirigir al login
    return redirect('login_template')

def cerrarSesion(request):
    logout(request)
    return redirect('login_template')


# ============================================================
# VISTAS DE TEMPLATES (Frontend) - NO MODIFICAR LAS DE ARRIBA
# ============================================================

def login_template(request):
    """Vista que renderiza el template de login/registro"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'auth/login.html')