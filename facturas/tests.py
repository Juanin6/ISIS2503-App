from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario
from reportes.models import Reporte
from datetime import date

class ReporteTests(TestCase):

    def setUp(self):
        # Crear un cliente para realizar solicitudes
        self.client = Client()

        # Crear un usuario administrador
        self.admin = Usuario.objects.create(
            correo="admin@example.com",
            contrasena="admin123",
            tipoUsuario="admin"
        )

        # Crear un usuario regular
        self.usuario = Usuario.objects.create(
            correo="user@example.com",
            contrasena="user123",
            tipoUsuario="estudiante"
        )

        # Crear reportes para pruebas
        self.reporte1 = Reporte.objects.create(
            concepto_pago="Pago de matrícula",
            valor_pagado=500.0,
            saldo_pendiente=0.0,
            fecha_emision=date(2024, 1, 1),
            id_estudiante=self.usuario
        )

        self.reporte2 = Reporte.objects.create(
            concepto_pago="Pago de biblioteca",
            valor_pagado=50.0,
            saldo_pendiente=0.0,
            fecha_emision=date(2024, 2, 1),
            id_estudiante=self.usuario
        )

    def test_autenticacion_usuario_correcto(self):
        """Prueba si un usuario regular puede autenticarse y ver sus reportes."""
        response = self.client.post(reverse('ver_reportes'), {
            'correo': 'user@example.com',
            'contrasena': 'user123'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('reportes', response.json())
        self.assertEqual(len(response.json()['reportes']), 2)

    def test_autenticacion_admin_correcto(self):
        """Prueba si un administrador puede autenticarse y ver todos los reportes."""
        response = self.client.post(reverse('ver_reportes'), {
            'correo': 'admin@example.com',
            'contrasena': 'admin123'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('reportes', response.json())
        self.assertGreaterEqual(len(response.json()['reportes']), 2)

    def test_autenticacion_fallida(self):
        """Prueba si el sistema rechaza usuarios con credenciales incorrectas."""
        response = self.client.post(reverse('ver_reportes'), {
            'correo': 'user@example.com',
            'contrasena': 'wrongpassword'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], "Credenciales inválidas")

    def test_tiempo_de_respuesta(self):
        """Prueba si el tiempo de respuesta está dentro del límite establecido."""
        import time
        inicio = time.time()

        response = self.client.post(reverse('ver_reportes'), {
            'correo': 'admin@example.com',
            'contrasena': 'admin123'
        }, content_type='application/json')

        fin = time.time()
        duracion = fin - inicio

        self.assertEqual(response.status_code, 200)
        self.assertLess(duracion, 3, "El tiempo de respuesta excede los 3 segundos")
