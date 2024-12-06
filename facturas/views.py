import json
from django.shortcuts import render
import requests
# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse
from reportes.models import Reporte
from .forms import FiltroReporteForm
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.shortcuts import render, redirect, get_object_or_404
from .models import Factura, Usuario
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Contraseña de administrador para verificar todas las facturas
ADMIN_PASSWORD = "admin_password123"  # Cambia esto a un valor seguro

@csrf_exempt
def ver_facturas(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Validar si es administrador
            if "password" in data and data["password"] == ADMIN_PASSWORD:
                facturas = Factura.objects.all()  # Recuperar todas las facturas
                facturas_data = [{"id": f.id, "detalle": f.detalle} for f in facturas]
                return JsonResponse({"response": "true", "facturas": facturas_data}, status=200)

            # Validar si es usuario regular
            elif "username" in data and "password" in data:
                usuario = Usuario.objects.get(username=data["username"], password=data["password"])
                facturas_usuario = Factura.objects.filter(usuario=usuario)
                facturas_data = [{"id": f.id, "detalle": f.detalle} for f in facturas_usuario]
                return JsonResponse({"response": "true", "facturas": facturas_data}, status=200)

            else:
                return JsonResponse({"response": "false", "message": "Credenciales incorrectas"}, status=403)
        except Usuario.DoesNotExist:
            return JsonResponse({"response": "false", "message": "Usuario no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"response": "false", "message": str(e)}, status=500)
    else:
        return JsonResponse({"response": "false", "message": "Método no permitido"}, status=405)
def admin_dashboard(request):
    if not request.user.is_staff:  # Verificar si es admin
        return HttpResponseForbidden("Acceso denegado")
    
    # Llamada al microservicio Flask
    response = requests.get('http://127.0.0.1:5000/admin/dashboard/')
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({'error': 'Error al comunicarse con el microservicio Flask'}, status=500)

def student_dashboard(request):
    if request.user.is_staff:  # Verificar que no sea admin
        return HttpResponseForbidden("Acceso denegado")
    
    # Llamada al microservicio Flask
    response = requests.get('http://127.0.0.1:5000/student/dashboard/')
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({'error': 'Error al comunicarse con el microservicio Flask'}, status=500)
def buscar_reportes(request):
    form = FiltroReporteForm(request.GET or None)
    
    if form.is_valid():
        id_estudiante = form.cleaned_data['id_estudiante']
        fecha_emision = form.cleaned_data['fecha_emision']
        concepto_pago = form.cleaned_data['concepto_pago']

        return redirect('generar_pdf', id_estudiante=id_estudiante, fecha_emision=fecha_emision, concepto_pago=concepto_pago)

    return render(request, 'facturas/buscar_reportes.html', {'form': form, 'previous_page': ""})

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

        p.setTitle(f"Reporte de {reportes.first().id_estudiante.nombre}")

        estudiante = reportes.first().id_estudiante

        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width / 2, height - 40, f"Reporte de {estudiante.nombre}")

        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, height - 70, "Fecha de emisión:")
        p.setFont("Helvetica", 12)
        p.drawString(220, height - 70, fecha_emision)

        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, height - 90, "Concepto:")
        p.setFont("Helvetica", 12)
        p.drawString(220, height - 90, concepto_pago)

        data = [['ID Reporte', 'ID Estudiante', 'Fecha Emisión', 'Concepto Pago', 'Valor Pagado', 'Pagado', 'Saldo Pendiente']]

        for reporte in reportes:
            data.append([
                reporte.id,
                f'{reporte.id_estudiante.nombre} ({reporte.id_estudiante.edad})',
                reporte.fecha_emision.strftime('%d/%m/%Y'),
                reporte.concepto_pago,
                reporte.valor_pagado,
                'Sí' if reporte.pagado else 'No',
                reporte.saldo_pendiente
            ])

        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ])
        table.setStyle(style)

        table_width, x = table.wrap(0, 0)
        x_position = (width - table_width) / 2

        table.wrapOn(p, width, height)
        table.drawOn(p, x_position, height - 170)

        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    return render(request, 'facturas/generar_pdf.html', {'reportes': reportes})

def verificar_integridad(request, reporte_id):
    # Obtén el reporte específico
    reporte = get_object_or_404(Reporte, id=reporte_id)
    
    # Recalcula el hash basado en los datos actuales
    hash_actual = reporte.calcular_hash()
    
    # Compara el hash actual con el almacenado
    if hash_actual != reporte.hash_integridad:
        # Redirige a una página de error si hay discrepancia
        return render(request, 'facturas/error_integridad.html', {'reporte': reporte})
    else:
        # Log the hashes for debugging
        print(f"Stored Hash: {reporte.hash_integridad}")
        print(f"Recalculated Hash: {hash_actual}")
        return render(request, 'facturas/reporte_integridad_verificada.html', {'reporte': reporte})

def verificar_integridad(request, reporte_id):
    # Obtén el reporte específico
    reporte = get_object_or_404(Reporte, id=reporte_id)
    
    # Recalcula el hash basado en los datos actuales
    hash_actual = reporte.calcular_hash()
    
    # Compara el hash actual con el almacenado
    if hash_actual != reporte.hash_integridad:
        # Redirige a una página de error si hay discrepancia
        return render(request, 'facturas/error_integridad.html', {'reporte': reporte})
    else:
        # Log the hashes for debugging
        print(f"Stored Hash: {reporte.hash_integridad}")
        print(f"Recalculated Hash: {hash_actual}")
        return render(request, 'facturas/reporte_integridad_verificada.html', {'reporte': reporte})
