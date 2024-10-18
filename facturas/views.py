from django.shortcuts import redirect, render
from django.http import HttpResponse
from reportes.models import Reporte
from .forms import FiltroReporteForm
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def buscar_reportes(request):
    form = FiltroReporteForm(request.GET or None)
    if form.is_valid():
        id_estudiante = form.cleaned_data['id_estudiante']
        fecha_emision = form.cleaned_data['fecha_emision']
        concepto_pago = form.cleaned_data['concepto_pago']

        return redirect('generar_pdf', id_estudiante=id_estudiante, fecha_emision=fecha_emision, concepto_pago=concepto_pago)

    return render(request, 'facturas/buscar_reportes.html', {'form': form})


def generar_pdf(request, id_estudiante, fecha_emision, concepto_pago):
    reportes = Reporte.objects.filter(
        id_estudiante=id_estudiante,
        fecha_emision=fecha_emision,
        concepto_pago=concepto_pago
    )

    if 'download_pdf' in request.GET:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        p.drawString(100, height - 100, f'Reporte para estudiante {id_estudiante} - Fecha Emisión {fecha_emision} - Concepto {concepto_pago}')

        y = height - 150
        for reporte in reportes:
            p.drawString(100, y, f'ID Reporte: {reporte.id} | Valor Pagado: {reporte.valor_pagado} | Saldo Pendiente: {reporte.saldo_pendiente}')
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    return render(request, 'facturas/generar_pdf.html', {'reportes': reportes})
