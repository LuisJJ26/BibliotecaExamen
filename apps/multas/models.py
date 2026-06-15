from django.db import models
from apps.prestamos.models import Prestamo
from apps.usuarios.models import Usuario

class Multa(models.Model):
    prestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE, related_name='multa')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='multas')
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_multa = models.DateTimeField(auto_now_add=True)
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return f"Multa {self.id} - {self.usuario.username} - ${self.monto}"

    def marcar_pagada(self):
        self.pagada = True
        self.save()