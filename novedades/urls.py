from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('gestionarnovedad/', views.GestionarNovedad),
    path('crearnovedad/', views.CrearNovedad)
]