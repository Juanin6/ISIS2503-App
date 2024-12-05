from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Factura

def admin_dashboard(request):
    if not request.user.is_staff:  # Verifica si es admin
        return HttpResponseForbidden("Acceso denegado")
    facturas = Factura.objects.all()
    return render(request, 'facturacion_microservicio/admin_dashboard.html', {'facturas': facturas})

def student_dashboard(request):
    if request.user.is_staff:  # Evita que los admins vean el panel de estudiantes
        return HttpResponseForbidden("Acceso denegado")
    facturas = Factura.objects.filter(usuario=request.user)
    return render(request, 'facturacion_microservicio/student_dashboard.html', {'facturas': facturas})
