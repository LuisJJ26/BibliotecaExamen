from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.usuarios.models import Usuario
from apps.libros.models import Ejemplar

class Prestamo(models.Model):
    ESTADO_PRESTAMO = (
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    )
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    estado_prestamo = models.CharField(max_length=10, choices=ESTADO_PRESTAMO, default='activo')
    renovaciones = models.IntegerField(default=0)

    def __str__(self):
        return f"Préstamo {self.id} - {self.usuario.username} - {self.ejemplar.codigo_barras}"

    def renovar(self, dias_extra=7):
        if self.estado_prestamo == 'activo' and self.renovaciones < 3:  # Máximo 3 renovaciones
            self.fecha_devolucion_esperada += timedelta(days=dias_extra)
            self.renovaciones += 1
            self.save()
            return True
        return False

    def devolver(self):
        from apps.multas.models import Multa  # Importación diferida para evitar circular
        self.fecha_devolucion_real = timezone.now()
        self.estado_prestamo = 'devuelto'
        self.ejemplar.devolver()  # Cambia estado del ejemplar a disponible
        self.save()

        # Generar multa si se retrasó
        if self.fecha_devolucion_real > self.fecha_devolucion_esperada:
            retraso_dias = (self.fecha_devolucion_real - self.fecha_devolucion_esperada).days
            monto = retraso_dias * 0.50  # Ejemplo: 0.50 por día de retraso
            Multa.objects.create(
                prestamo=self,
                usuario=self.usuario,
                monto=monto,
                fecha_multa=timezone.now(),
                pagada=False
            )
        return True