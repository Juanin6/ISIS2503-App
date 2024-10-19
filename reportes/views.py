from django.shortcuts import redirect, render
from usuarios.models import Usuario

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