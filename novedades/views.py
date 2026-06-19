from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def Home(request):
    return HttpResponse("Novedades")

def CrearNovedad(request):
    return HttpResponse("Crea Novedades Aquí")

def GestionarNovedad(request):
    return HttpResponse("Gestiona Novedades Aquí")