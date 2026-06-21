from django.urls import path
from . import views

urlpatterns = [
    path('',views.iniciarSesion),
    path('registro/',views.registrarse),
    path('cerrarSesion/',views.cerrarSesion)
]