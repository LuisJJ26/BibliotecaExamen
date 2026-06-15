from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.mixins import BibliotecarioRequiredMixin
from .models import Prestamo
from .forms import PrestamoForm
from datetime import timedelta

class PrestamoListView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'prestamos/prestamo_list.html'
    context_object_name = 'prestamos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol == 'usuario':
            queryset = queryset.filter(usuario=self.request.user)
        # Bibliotecario y admin ven todos
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado_prestamo=estado)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(usuario__username__icontains=q) | queryset.filter(ejemplar__codigo_barras__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = Prestamo.ESTADO_PRESTAMO
        return context

class PrestamoCreateView(BibliotecarioRequiredMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamos/prestamo_form.html'
    success_url = reverse_lazy('prestamos:list')

    def form_valid(self, form):
        prestamo = form.save(commit=False)
        prestamo.fecha_devolucion_esperada = timezone.now() + timedelta(days=7)
        prestamo.save()
        ejemplar = prestamo.ejemplar
        ejemplar.estado = 'prestado'
        ejemplar.save()
        messages.success(self.request, 'Préstamo registrado correctamente.')
        return super().form_valid(form)

class PrestamoDevolverView(BibliotecarioRequiredMixin, UpdateView):
    model = Prestamo
    fields = []
    template_name = 'prestamos/prestamo_confirm_devolver.html'

    def post(self, request, *args, **kwargs):
        prestamo = self.get_object()
        prestamo.devolver()
        messages.success(request, 'Devolución registrada. Se generó multa si aplicaba.')
        return redirect('prestamos:list')

class PrestamoRenovarView(BibliotecarioRequiredMixin, UpdateView):
    model = Prestamo
    fields = []
    template_name = 'prestamos/prestamo_confirm_renovar.html'

    def post(self, request, *args, **kwargs):
        prestamo = self.get_object()
        if prestamo.renovar():
            messages.success(request, 'Préstamo renovado exitosamente.')
        else:
            messages.error(request, 'No se pudo renovar (máximo 3 renovaciones o préstamo no activo).')
        return redirect('prestamos:list')

# ... tus otras vistas de préstamos (PrestamoListView, PrestamoCreateView, etc.) ...

# Funciones AJAX para búsqueda
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.libros.models import Ejemplar

User = get_user_model()

def buscar_usuarios_ajax(request):
    term = request.GET.get('term', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    usuarios = User.objects.all()
    if term:
        usuarios = usuarios.filter(
            Q(username__icontains=term) |
            Q(email__icontains=term) |
            Q(first_name__icontains=term) |
            Q(last_name__icontains=term)
        )
    
    start = (page - 1) * page_size
    end = start + page_size
    usuarios_page = usuarios[start:end]
    
    results = [{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'rol': u.get_rol_display(),
    } for u in usuarios_page]
    
    more = len(usuarios) > end
    
    return JsonResponse({
        'results': results,
        'more': more,
    })

def buscar_ejemplares_ajax(request):
    term = request.GET.get('term', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    ejemplares = Ejemplar.objects.select_related('libro')
    if term:
        ejemplares = ejemplares.filter(
            Q(codigo_barras__icontains=term) |
            Q(libro__titulo__icontains=term)
        )
    # Solo ejemplares disponibles
    ejemplares = ejemplares.filter(estado='disponible')
    
    start = (page - 1) * page_size
    end = start + page_size
    ejemplares_page = ejemplares[start:end]
    
    results = [{
        'id': e.id,
        'codigo_barras': e.codigo_barras,
        'libro_titulo': e.libro.titulo,
        'estado': e.estado,
    } for e in ejemplares_page]
    
    more = len(ejemplares) > end
    
    return JsonResponse({
        'results': results,
        'more': more,
    })