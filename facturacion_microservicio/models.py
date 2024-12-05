from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Admin'),
        ('estudiante', 'Estudiante'),
    ]
    tipoUsuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='estudiante')
