from django import forms
from datetime import datetime

# Opciones para Concepto de Pago
CONCEPTO_PAGO_CHOICES = [
    ('pension', 'Pensión'),
    ('matricula', 'Matrícula'),
    ('extracurriculares', 'Extracurriculares'),
]

# Función para generar las fechas de emisión (primer día de cada mes durante los últimos dos años)
def generar_fechas_emision():
    opciones = []
    today = datetime.today()
    for i in range(24):
        mes = (today.month - i - 1) % 12 + 1
        año = today.year - ((today.month - i - 1) // 12)
        opciones.append((f'{año}-{mes:02d}-01', f'01/{mes:02d}/{año}'))
    return opciones

class FiltroReporteForm(forms.Form):
    id_estudiante = forms.IntegerField(label='ID Estudiante')

    # Desplegable para FechaEmision
    fecha_emision = forms.ChoiceField(
        label='Fecha de Emisión',
        choices=generar_fechas_emision(),
        widget=forms.Select
    )

    # Desplegable para ConceptoDePago
    concepto_pago = forms.ChoiceField(
        label='Concepto de Pago',
        choices=CONCEPTO_PAGO_CHOICES,
        widget=forms.Select
    )
