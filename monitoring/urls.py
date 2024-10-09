from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    path('reporte/', views.generar_reporte, name='generar_reporte'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
]
