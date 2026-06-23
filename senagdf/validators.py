import re

def validar_documento(documento):
    # El documento solo puede tener 10 dígitos
    patron = r'^\d{10}$'
    return re.match(patron, documento) is not None

def validar_nombre(texto):
    # Nombres y apellidos: solo letras (con tildes, ñ), espacios, máximo 45 caracteres
    patron = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{1,45}$'
    return re.match(patron, texto) is not None

def validar_celular(celular):
    # El celular solo puede tener 10 dígitos
    patron = r'^3\d{9}$'
    return re.match(patron, celular) is not None

def validar_correo(correo):
    # El email debe mandarse completo como por ejemplo hola@gmail.com
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None