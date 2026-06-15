from django import forms
from .models import Libro, Ejemplar, Categoria

class LibroForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'editorial', 'año_publicacion', 'isbn', 'ubicacion', 'descripcion', 'categorias']

class EjemplarForm(forms.ModelForm):
    class Meta:
        model = Ejemplar
        fields = ['codigo_barras', 'estado']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']