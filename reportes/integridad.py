import threading
import time
from .models import Reporte

def verificar_integridad():
    while True:
        time.sleep(20)  # Intervalo de verificación
        reportes = Reporte.objects.all()
        for reporte in reportes:
            hash_actual = reporte.calcular_hash()
            if hash_actual != reporte.hash_integridad:
                print(f"Error de integridad en el reporte ID {reporte.id}")
                # Aquí puedes agregar lógica para generar un aviso en la interfaz
