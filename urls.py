from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el administrador de Django
    path('', include('monitoring.urls')),  # Incluir las URLs de tu aplicación
]
