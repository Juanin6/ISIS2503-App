from django.urls import path
from . import views

urlpatterns = [
    path('facturas/', views.buscar_reportes, name='buscar_reportes')
]
