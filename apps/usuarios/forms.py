from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre', 'telefono', 'direccion', 'rol', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets si se desea

class UsuarioChangeForm(UserChangeForm):
    password = None  # No mostrar campo password en edición
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre', 'telefono', 'direccion', 'rol')