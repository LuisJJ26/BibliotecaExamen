from django import forms
from .models import Prestamo
from apps.usuarios.models import Usuario
from apps.libros.models import Ejemplar

class PrestamoForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.filter(rol='usuario'), label="Usuario")
    ejemplar = forms.ModelChoiceField(queryset=Ejemplar.objects.filter(estado='disponible'), label="Ejemplar")
    
    class Meta:
        model = Prestamo
        fields = ['usuario', 'ejemplar']