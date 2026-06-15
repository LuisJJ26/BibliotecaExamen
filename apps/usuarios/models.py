from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('administrador', 'Administrador'),
        ('bibliotecario', 'Bibliotecario'),
        ('usuario', 'Usuario'),
    )
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # El campo email ya existe en AbstractUser, lo forzamos a único
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"