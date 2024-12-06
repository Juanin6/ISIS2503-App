from django.urls import path
from . import views

urlpatterns = [
    path('facturas/', views.buscar_reportes, name='buscar_reportes'),
    path('facturas/generar-pdf/<int:id_estudiante>/<str:fecha_emision>/<str:concepto_pago>/', views.generar_pdf, name='generar_pdf'),
    path('factura/<int:reporte_id>/verificar_integridad/', views.verificar_integridad, name='verificar_integridad'),
    path('ver-facturas/', views.ver_reportes, name='ver_facturas'),
]
