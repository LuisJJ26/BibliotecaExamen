#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model

User = get_user_model()

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
"