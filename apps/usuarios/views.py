from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from apps.core.mixins import AdminRequiredMixin
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.libros.models import Libro, Ejemplar
from apps.prestamos.models import Prestamo
from apps.multas.models import Multa
from django.contrib.auth import get_user_model

class LoginView(AuthLoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('login')

User = get_user_model()
class HomeView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['home.html']  # panel de control
        return ['home_landing.html']  # landing page pública

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Datos públicos para estadísticas (siempre se calculan)
        from apps.libros.models import Libro, Ejemplar
        from apps.prestamos.models import Prestamo
        from apps.multas.models import Multa
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        context['total_libros'] = Libro.objects.count()
        context['total_ejemplares'] = Ejemplar.objects.count()
        context['total_prestamos_activos'] = Prestamo.objects.filter(estado_prestamo='activo').count()
        context['total_usuarios'] = User.objects.count()

        # Si está autenticado, agregamos datos específicos del dashboard
        if self.request.user.is_authenticated:
            user = self.request.user
            if user.rol == 'administrador':
                context['prestamos_activos'] = context['total_prestamos_activos']
                context['multas_pendientes'] = Multa.objects.filter(pagada=False).count()
            elif user.rol == 'bibliotecario':
                context['prestamos_activos'] = context['total_prestamos_activos']
                context['multas_pendientes'] = Multa.objects.filter(pagada=False).count()
            else:  # usuario normal
                context['mis_prestamos_activos'] = user.prestamos.filter(estado_prestamo='activo').count()
                context['mis_multas_pendientes'] = user.multas.filter(pagada=False).count()
        return context

# Solo administrador puede listar, crear, editar, eliminar usuarios
class UsuarioListView(AdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(username__icontains=q) | queryset.filter(email__icontains=q)
        return queryset

class UsuarioCreateView(AdminRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado exitosamente.')
        return super().form_valid(form)

class UsuarioUpdateView(AdminRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioChangeForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado correctamente.')
        return super().form_valid(form)

class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuario eliminado.')
        return super().delete(request, *args, **kwargs)