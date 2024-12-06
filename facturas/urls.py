from django.urls import path
from . import views

urlpatterns = [
    path('facturas/manejador/', views.buscar_reportes, name='buscar_reportes'),
    path('facturas/', views.buscar_reportes2, name='buscar_reportes_pdf'),
    path('facturas/generar-pdf/<int:id_estudiante>/<str:fecha_emision>/<str:concepto_pago>/', views.generar_pdf, name='generar_pdf'),
    path('ver-reportes/', views.ver_reportes, name='ver_reportes'),
]
