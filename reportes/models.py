import hashlib
from django.db import models
from usuarios.models import Usuario

class Reporte(models.Model):
    id_estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True)
    concepto_pago = models.CharField(max_length=50)
    valor_pagado = models.IntegerField(default=0)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(null=True, blank=True) 
    descuento_aplicado = models.IntegerField(default=0)
    saldo_pendiente = models.IntegerField(default=0)

    # Nuevo campo para almacenar el hash de integridad
    hash_integridad = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.hash_integridad:
            self.hash_integridad = self.calcular_hash()
        super().save(*args, **kwargs)

    def calcular_hash(self):
        # Genera un hash a partir de los datos importantes del reporte
        hash_data = f"{self.fecha_emision}{self.concepto_pago}{self.valor_pagado}{self.saldo_pendiente}".encode('utf-8')
        return hashlib.sha256(hash_data).hexdigest()