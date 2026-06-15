from django.contrib import admin
from .models import Categoria, Libro, LibroCategoria, Ejemplar

admin.site.register(Categoria)
admin.site.register(Libro)
admin.site.register(LibroCategoria)
admin.site.register(Ejemplar)