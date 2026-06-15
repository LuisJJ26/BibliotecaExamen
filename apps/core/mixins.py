from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo administradores pueden acceder a vistas de creación/edición/eliminación de recursos críticos."""
    def test_func(self):
        return self.request.user.rol == 'administrador'
    
    def handle_no_permission(self):
        raise PermissionDenied("No tienes permisos de administrador.")

class BibliotecarioRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Administradores y bibliotecarios pueden gestionar préstamos y multas."""
    def test_func(self):
        return self.request.user.rol in ['administrador', 'bibliotecario']
    
    def handle_no_permission(self):
        raise PermissionDenied("No tienes permisos para gestionar préstamos o multas.")