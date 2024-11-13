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
    # Campo nuevo para el hash de integridad
    hash_integridad = models.CharField(max_length=64, blank=True)
 

def calcular_hash(self):
        # Concatena los datos para generar el hash
        data = f"{self.id_usuario_id}{self.fecha_emision}{self.concepto_pago}{self.valor_pagado}{self.pagado}{self.saldo_pendiente}"
        return hashlib.sha256(data.encode()).hexdigest()

def save(self, *args, **kwargs):
    # Calcula y guarda el hash antes de guardar el objeto
    self.hash_integridad = self.calcular_hash()
    super(Reporte, self).save(*args, **kwargs)