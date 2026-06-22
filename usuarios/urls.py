from django.urls import path
from . import views

urlpatterns = [
    # API endpoints - NO MODIFICAR
    path('', views.iniciarSesion, name='login_api'),
    path('registro/', views.registrarse, name='registro_api'),
    path('cerrarSesion/', views.cerrarSesion, name='cerrar_sesion'),
    # Template views (Frontend)
    path('login/', views.login_template, name='login_template'),
]