# -*- coding: utf-8 -*-
import random
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Cambia 'config' por tu proyecto

import django
django.setup()

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from apps.libros.models import Categoria, Libro, LibroCategoria, Ejemplar
from apps.usuarios.models import Usuario
from apps.prestamos.models import Prestamo
from apps.multas.models import Multa

print("Limpiando datos (excepto superusuario)...")
Prestamo.objects.all().delete()
Multa.objects.all().delete()
Ejemplar.objects.all().delete()
LibroCategoria.objects.all().delete()
Libro.objects.all().delete()
Categoria.objects.all().delete()
Usuario.objects.exclude(is_superuser=True).delete()

print("Creando 30 categorias...")
categorias = []
for i in range(1, 31):
    nombre = f"Categoria_{i}"
    cat = Categoria.objects.create(nombre=nombre, descripcion=f"Descripcion de {nombre}")
    categorias.append(cat)

print("Creando 30 libros...")
libros = []
for i in range(1, 31):
    isbn = f"978{random.randint(100000000, 999999999)}"[:13]
    libro = Libro.objects.create(
        titulo=f"Libro {i}",
        autor=f"Autor {random.choice(['A','B','C','D'])}{i}",
        editorial=f"Editorial {random.randint(1,10)}",
        año_publicacion=random.randint(1950, 2023),
        isbn=isbn,
        ubicacion=f"Estante {random.choice(['A','B','C'])}-{random.randint(1,10)}",
        descripcion=f"Descripcion del libro {i}"
    )
    libros.append(libro)

print("Asignando categorias a los libros...")
for libro in libros:
    num_cats = random.randint(1, 3)
    cats_elegidas = random.sample(categorias, num_cats)
    for cat in cats_elegidas:
        LibroCategoria.objects.create(libro=libro, categoria=cat)

print("Creando 30 ejemplares...")
ejemplares = []
for i in range(1, 31):
    libro = random.choice(libros)
    estado = random.choices(['disponible','prestado','extraviado','en_reparacion'], weights=[0.7,0.2,0.05,0.05])[0]
    ejem = Ejemplar.objects.create(libro=libro, codigo_barras=f"EJE-{i:04d}", estado=estado)
    ejemplares.append(ejem)

print("Creando 30 usuarios...")
usuarios = []
for i in range(1, 31):
    user = Usuario.objects.create(
        username=f"user_{i}",
        email=f"user{i}@example.com",
        nombre=f"Nombre {i}",
        telefono=f"555-{random.randint(1000,9999)}",
        direccion=f"Calle {random.randint(1,100)}, Ciudad",
        rol=random.choices(['administrador','bibliotecario','usuario'], weights=[0.1,0.2,0.7])[0],
        password=make_password('password123')
    )
    usuarios.append(user)

print("Creando prestamos (al menos 30)...")
prestamos_creados = 0
intentos = 0
while prestamos_creados < 30 and intentos < 200:
    intentos += 1
    ejemplar = random.choice(ejemplares)
    usuario = random.choice(usuarios)
    if ejemplar.estado == 'disponible':
        fecha_prestamo = timezone.now() - timedelta(days=random.randint(0, 60))
        dias_espera = random.randint(7, 30)
        fecha_esperada = fecha_prestamo + timedelta(days=dias_espera)
        estado_opcion = random.choices(['activo','devuelto','vencido'], weights=[0.5,0.4,0.1])[0]
        fecha_real = None
        if estado_opcion == 'devuelto':
            if random.random() < 0.5:
                fecha_real = fecha_esperada - timedelta(days=random.randint(1,5))
            else:
                fecha_real = fecha_esperada + timedelta(days=random.randint(1,15))
            if fecha_real > timezone.now():
                fecha_real = timezone.now()
            estado_final = 'devuelto'
        elif estado_opcion == 'vencido':
            if fecha_esperada > timezone.now():
                fecha_esperada = timezone.now() - timedelta(days=random.randint(1,10))
            estado_final = 'vencido'
        else:
            estado_final = 'activo'

        prestamo = Prestamo.objects.create(
            ejemplar=ejemplar,
            usuario=usuario,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion_esperada=fecha_esperada,
            fecha_devolucion_real=fecha_real,
            estado_prestamo=estado_final,
            renovaciones=random.randint(0,3) if estado_final=='activo' else 0
        )
        prestamos_creados += 1

        if estado_final == 'devuelto':
            ejemplar.estado = 'disponible'
            ejemplar.save()
            if fecha_real and fecha_real > fecha_esperada:
                retraso = (fecha_real - fecha_esperada).days
                Multa.objects.create(
                    prestamo=prestamo,
                    usuario=usuario,
                    monto=retraso * 0.50,
                    pagada=random.choice([True,False])
                )
        else:
            ejemplar.estado = 'prestado'
            ejemplar.save()

print(f"Prestamos creados: {prestamos_creados}")

# Asegurar al menos 30 multas
multas_actuales = Multa.objects.count()
if multas_actuales < 30:
    print(f"Creando {30-multas_actuales} multas adicionales...")
    prestamos_devueltos = Prestamo.objects.filter(estado_prestamo='devuelto', multa__isnull=True)
    for p in prestamos_devueltos:
        if p.fecha_devolucion_real and p.fecha_devolucion_real > p.fecha_devolucion_esperada:
            retraso = (p.fecha_devolucion_real - p.fecha_devolucion_esperada).days
            Multa.objects.create(
                prestamo=p,
                usuario=p.usuario,
                monto=retraso * 0.50,
                pagada=random.choice([True,False])
            )
            if Multa.objects.count() >= 30:
                break

    while Multa.objects.count() < 30:
        ejem_disponible = Ejemplar.objects.filter(estado='disponible').first()
        if not ejem_disponible:
            ejem_disponible = Ejemplar.objects.create(
                libro=random.choice(libros),
                codigo_barras=f"TEMP-{random.randint(1000,9999)}",
                estado='disponible'
            )
            ejemplares.append(ejem_disponible)
        usuario = random.choice(usuarios)
        fecha_prestamo = timezone.now() - timedelta(days=random.randint(10,30))
        fecha_esperada = fecha_prestamo + timedelta(days=7)
        fecha_real = fecha_esperada + timedelta(days=random.randint(1,10))
        prestamo = Prestamo.objects.create(
            ejemplar=ejem_disponible,
            usuario=usuario,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion_esperada=fecha_esperada,
            fecha_devolucion_real=fecha_real,
            estado_prestamo='devuelto'
        )
        ejem_disponible.estado = 'disponible'
        ejem_disponible.save()
        retraso = (fecha_real - fecha_esperada).days
        Multa.objects.create(
            prestamo=prestamo,
            usuario=usuario,
            monto=retraso * 0.50,
            pagada=random.choice([True,False])
        )

print("Verificacion final:")
print(f"Categorias: {Categoria.objects.count()}")
print(f"Libros: {Libro.objects.count()}")
print(f"LibroCategoria: {LibroCategoria.objects.count()}")
print(f"Ejemplares: {Ejemplar.objects.count()}")
print(f"Usuarios: {Usuario.objects.count()}")
print(f"Prestamos: {Prestamo.objects.count()}")
print(f"Multas: {Multa.objects.count()}")
print("Poblacion completada.")