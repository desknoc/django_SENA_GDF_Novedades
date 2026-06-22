from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuarios_views
from novedades import views as novedades_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usuarios_views.login_template, name='login_template'),
    path('usuarios/', include('usuarios.urls')),
    path('novedades/', include('novedades.urls')),
    path('404/', novedades_views.error404_template, name='error404'),
]