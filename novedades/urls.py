from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('editar/<int:id>/', views.EditarNovedad), #Buscamos por id
    path('crearnovedad/', views.CrearNovedad)
]