from django.http import HttpResponse
from django.shortcuts import redirect, render
from usuarios.models import Usuario
import threading
from .integridad import verificar_integridad
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


# Controla que solo se inicie un hilo de verificación
verificacion_iniciada = False
def inicio_reportes(request):
        global verificacion_iniciada
        if not verificacion_iniciada:
            verificador = threading.Thread(target=verificar_integridad)
            verificador.daemon = True
            verificador.start()
            verificacion_iniciada = True

        return render(request, 'reportes/reportes.html')
