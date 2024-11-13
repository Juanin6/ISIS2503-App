from django.shortcuts import redirect, render
from usuarios.models import Usuario
from django.http import JsonResponse
from .models import Reporte

def inicio_reportes(request):
    return render(request, 'reportes/reportes.html')

def reporte_usuario(request):
    correo = request.GET.get('correo')
    usuario = None

    if correo:
        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            usuario = None

    if usuario:
        return render(request, 'reportes/reporte_usuarios.html', {'usuario': usuario})
    else:
        return render(request, 'reportes/usuario_no_encontrado.html')


def back_view(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('user_reports')


def verificar_integridad_reportes(request):
    reportes = Reporte.objects.all()
    errores_integridad = []

    for reporte in reportes:
        hash_actual = reporte.calcular_hash()
        if hash_actual != reporte.hash_integridad:
            errores_integridad.append(f"Error de integridad en el reporte ID {reporte.id}")

    # Si hay errores, los enviamos al template
    if errores_integridad:
        return render(request, 'reportes.html', {'error_integridad': "Se ha realizado un ataque de integridad."})
    else:
        return render(request, 'reportes.html')