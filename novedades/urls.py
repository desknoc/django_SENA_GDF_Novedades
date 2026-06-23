from django.urls import path
from . import views

urlpatterns = [
    # API endpoints (JSON) - NO MODIFICAR
    path('', views.Home, name='home'),
    path('editar/<int:id>/', views.EditarNovedad),
    path('crearnovedad/', views.CrearNovedad),
    path('eliminarnovedad/<int:id>/', views.EliminarNovedad),
    path('detallenovedad/<int:id>/', views.DetalleNovedad),
    # Template views (Frontend)
    path('detalle/<int:id>/', views.detalle_template, name='detalle_novedad'),
    path('admin/', views.admin_novedades_template, name='admin_novedades'),
    path('admin/crear/', views.admin_novedad_crear_template, name='admin_novedad_crear'),
    path('admin/editar/<int:id>/', views.admin_novedad_editar_template, name='admin_novedad_editar'),
]