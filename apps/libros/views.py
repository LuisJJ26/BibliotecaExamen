from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from apps.core.mixins import AdminRequiredMixin
from .models import Libro, Ejemplar, Categoria
from .forms import LibroForm, EjemplarForm, CategoriaForm

# ---------- Libros ----------
class LibroListView(AdminRequiredMixin, ListView):
    model = Libro
    template_name = 'libros/libro_list.html'
    context_object_name = 'libros'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(titulo__icontains=q) | queryset.filter(autor__icontains=q) | queryset.filter(isbn__icontains=q)
        return queryset

class LibroDetailView(AdminRequiredMixin, DetailView):
    model = Libro
    template_name = 'libros/libro_detail.html'
    context_object_name = 'libro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ejemplares'] = self.object.ejemplares.all()
        context['categorias'] = self.object.categorias.all()
        return context

class LibroCreateView(AdminRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('libros:list')

    def form_valid(self, form):
        messages.success(self.request, 'Libro creado exitosamente.')
        response = super().form_valid(form)
        self.object.categorias.set(form.cleaned_data['categorias'])
        return response

class LibroUpdateView(AdminRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('libros:list')

    def form_valid(self, form):
        messages.success(self.request, 'Libro actualizado correctamente.')
        response = super().form_valid(form)
        self.object.categorias.set(form.cleaned_data['categorias'])
        return response

class LibroDeleteView(AdminRequiredMixin, DeleteView):
    model = Libro
    template_name = 'libros/libro_confirm_delete.html'
    success_url = reverse_lazy('libros:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Libro eliminado.')
        return super().delete(request, *args, **kwargs)

# ---------- Ejemplares ----------
class EjemplarListView(AdminRequiredMixin, ListView):
    model = Ejemplar
    template_name = 'libros/ejemplar_list.html'
    context_object_name = 'ejemplares'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(codigo_barras__icontains=q) | queryset.filter(libro__titulo__icontains=q)
        libro_id = self.request.GET.get('libro')
        if libro_id:
            queryset = queryset.filter(libro_id=libro_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro_id = self.request.GET.get('libro')
        if libro_id:
            context['libro'] = get_object_or_404(Libro, pk=libro_id)
        return context

class EjemplarCreateView(AdminRequiredMixin, CreateView):
    model = Ejemplar
    form_class = EjemplarForm
    template_name = 'libros/ejemplar_form.html'

    def get_success_url(self):
        return reverse_lazy('libros:detail', kwargs={'pk': self.object.libro.pk})

    def form_valid(self, form):
        libro_id = self.kwargs.get('libro_id')
        form.instance.libro = get_object_or_404(Libro, pk=libro_id)
        messages.success(self.request, 'Ejemplar creado exitosamente.')
        return super().form_valid(form)

class EjemplarUpdateView(AdminRequiredMixin, UpdateView):
    model = Ejemplar
    form_class = EjemplarForm
    template_name = 'libros/ejemplar_form.html'

    def get_success_url(self):
        return reverse_lazy('libros:detail', kwargs={'pk': self.object.libro.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Ejemplar actualizado.')
        return super().form_valid(form)

class EjemplarDeleteView(AdminRequiredMixin, DeleteView):
    model = Ejemplar
    template_name = 'libros/ejemplar_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('libros:detail', kwargs={'pk': self.object.libro.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ejemplar eliminado.')
        return super().delete(request, *args, **kwargs)

# ---------- Categorías ----------
class CategoriaListView(AdminRequiredMixin, ListView):
    model = Categoria
    template_name = 'libros/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        return queryset

class CategoriaCreateView(AdminRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'libros/categoria_form.html'
    success_url = reverse_lazy('libros:categoria_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada.')
        return super().form_valid(form)

class CategoriaUpdateView(AdminRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'libros/categoria_form.html'
    success_url = reverse_lazy('libros:categoria_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada.')
        return super().form_valid(form)

class CategoriaDeleteView(AdminRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'libros/categoria_confirm_delete.html'
    success_url = reverse_lazy('libros:categoria_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoría eliminada.')
        return super().delete(request, *args, **kwargs)

