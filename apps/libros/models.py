from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editorial = models.CharField(max_length=100)
    año_publicacion = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    ubicacion = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    categorias = models.ManyToManyField(Categoria, through='LibroCategoria')

    def __str__(self):
        return self.titulo

class LibroCategoria(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('libro', 'categoria')

    def __str__(self):
        return f"{self.libro.titulo} - {self.categoria.nombre}"

class Ejemplar(models.Model):
    ESTADO_CHOICES = (
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('extraviado', 'Extraviado'),
        ('en_reparacion', 'En Reparacion'),
    )
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='ejemplares')
    codigo_barras = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')

    def __str__(self):
        return f"Ejemplar {self.codigo_barras} - {self.libro.titulo}"

    # Reglas de negocio
    def prestar(self):
        if self.estado == 'disponible':
            self.estado = 'prestado'
            self.save()
            return True
        return False

    def devolver(self):
        if self.estado == 'prestado':
            self.estado = 'disponible'
            self.save()
            return True
        return False

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADO_CHOICES):
            self.estado = nuevo_estado
            self.save()
            return True
        return False