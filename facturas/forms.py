from django import forms
from datetime import datetime

CONCEPTO_PAGO = [
    ('Pensión', 'Pensión'),
    ('Matrícula', 'Matrícula'),
    ('Extracurriculares', 'Extracurriculares'),
]

class FiltroReporteForm(forms.Form):
    id_estudiante = forms.IntegerField(label='ID Estudiante')

    fecha_emision = forms.DateField(
        label='Fecha de Emisión',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    concepto_pago = forms.ChoiceField(
        label='Concepto de Pago',
        choices=CONCEPTO_PAGO,
        widget=forms.Select
    )
    
