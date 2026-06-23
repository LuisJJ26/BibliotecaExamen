#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
from apps.libros.models import Libro

User = get_user_model()

# Superusuario
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@biblioteca.com',
        password='Admin123456',
        nombre='Administrador'
    )
    print('Superusuario creado')
else:
    print('Superusuario ya existe')

# Lista de 20 libros (con los campos que tienes en tu modelo)
libros = [
    {'titulo': 'Cien años de soledad', 'autor': 'Gabriel García Márquez', 'isbn': '978-84-376-0494-7', 'genero': 'Novela', 'año_publicacion': 1967},
    {'titulo': 'El amor en los tiempos del cólera', 'autor': 'Gabriel García Márquez', 'isbn': '978-84-376-0495-4', 'genero': 'Novela', 'año_publicacion': 1985},
    {'titulo': 'Don Quijote de la Mancha', 'autor': 'Miguel de Cervantes', 'isbn': '978-84-206-4450-9', 'genero': 'Novela', 'año_publicacion': 1605},
    {'titulo': 'La casa de los espíritus', 'autor': 'Isabel Allende', 'isbn': '978-84-322-0300-0', 'genero': 'Novela', 'año_publicacion': 1982},
    {'titulo': 'Rayuela', 'autor': 'Julio Cortázar', 'isbn': '978-84-322-0801-2', 'genero': 'Novela', 'año_publicacion': 1963},
    {'titulo': 'El principio del placer', 'autor': 'José Emilio Pacheco', 'isbn': '978-84-322-0999-6', 'genero': 'Cuento', 'año_publicacion': 1972},
    {'titulo': 'La sombra del viento', 'autor': 'Carlos Ruiz Zafón', 'isbn': '978-84-204-5750-5', 'genero': 'Novela', 'año_publicacion': 2001},
    {'titulo': 'El juego del ángel', 'autor': 'Carlos Ruiz Zafón', 'isbn': '978-84-204-6963-8', 'genero': 'Novela', 'año_publicacion': 2008},
    {'titulo': 'El prisionero del cielo', 'autor': 'Carlos Ruiz Zafón', 'isbn': '978-84-204-0699-8', 'genero': 'Novela', 'año_publicacion': 2011},
    {'titulo': 'El laberinto de los espíritus', 'autor': 'Carlos Ruiz Zafón', 'isbn': '978-84-204-2660-8', 'genero': 'Novela', 'año_publicacion': 2016},
    {'titulo': 'Crónica de una muerte anunciada', 'autor': 'Gabriel García Márquez', 'isbn': '978-84-376-0496-1', 'genero': 'Novela', 'año_publicacion': 1981},
    {'titulo': 'El coronel no tiene quien le escriba', 'autor': 'Gabriel García Márquez', 'isbn': '978-84-376-0497-8', 'genero': 'Novela', 'año_publicacion': 1961},
    {'titulo': 'La tregua', 'autor': 'Mario Benedetti', 'isbn': '978-84-322-0301-7', 'genero': 'Novela', 'año_publicacion': 1960},
    {'titulo': 'El túnel', 'autor': 'Ernesto Sabato', 'isbn': '978-84-322-0302-4', 'genero': 'Novela', 'año_publicacion': 1948},
    {'titulo': 'Sobre héroes y tumbas', 'autor': 'Ernesto Sabato', 'isbn': '978-84-322-0303-1', 'genero': 'Novela', 'año_publicacion': 1961},
    {'titulo': 'Abaddón el exterminador', 'autor': 'Ernesto Sabato', 'isbn': '978-84-322-0304-8', 'genero': 'Novela', 'año_publicacion': 1974},
    {'titulo': 'El Aleph', 'autor': 'Jorge Luis Borges', 'isbn': '978-84-322-0305-5', 'genero': 'Cuento', 'año_publicacion': 1949},
    {'titulo': 'Ficciones', 'autor': 'Jorge Luis Borges', 'isbn': '978-84-322-0306-2', 'genero': 'Cuento', 'año_publicacion': 1944},
    {'titulo': 'El libro de arena', 'autor': 'Jorge Luis Borges', 'isbn': '978-84-322-0307-9', 'genero': 'Cuento', 'año_publicacion': 1975},
    {'titulo': 'La invención de Morel', 'autor': 'Adolfo Bioy Casares', 'isbn': '978-84-322-0308-6', 'genero': 'Novela', 'año_publicacion': 1940},
]

creados = 0
existentes = 0
for libro_data in libros:
    # Usamos get_or_create por ISBN
    obj, created = Libro.objects.get_or_create(
        isbn=libro_data['isbn'],
        defaults={k: v for k, v in libro_data.items() if k != 'isbn'}
    )
    if created:
        creados += 1
    else:
        existentes += 1

print(f'Libros: {creados} creados, {existentes} ya existían')
"

# Nota: Si tu modelo tiene campos obligatorios no listados (ej. editorial, ubicacion, etc.),
# deberás agregarlos a los diccionarios o hacerlos opcionales en el modelo.