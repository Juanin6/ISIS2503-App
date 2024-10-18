from django import forms
from datetime import datetime

CONCEPTO_PAGO = [
    ('pension', 'Pensión'),
    ('matricula', 'Matrícula'),
    ('extracurriculares', 'Extracurriculares'),
]

def generar_fechas_emision():
    opciones = []
    today = datetime.today()
    for i in range(24):
        mes = (today.month - i - 1) % 12 + 1
        anio = today.year - ((today.month - i - 1) // 12)
        opciones.append((f'{anio}-{mes:02d}-01', f'01/{mes:02d}/{anio}'))
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
        choices=CONCEPTO_PAGO,
        widget=forms.Select
    )
