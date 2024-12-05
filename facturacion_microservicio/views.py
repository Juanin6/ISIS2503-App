from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.views import View
from .models import Factura

class AdminDashboard(View):
    def get(self, request):
        if request.user.tipoUsuario != 'admin':
            return HttpResponseForbidden("Acceso denegado")
        facturas = Factura.objects.all()
        return render(request, 'admin_dashboard.html', {'facturas': facturas})

class StudentDashboard(View):
    def get(self, request):
        if request.user.tipoUsuario != 'estudiante':
            return HttpResponseForbidden("Acceso denegado")
        facturas = Factura.objects.filter(usuario=request.user)
        return render(request, 'student_dashboard.html', {'facturas': facturas})
