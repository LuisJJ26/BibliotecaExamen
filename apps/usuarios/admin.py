from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información extra', {'fields': ('telefono', 'direccion', 'rol')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información extra', {'fields': ('telefono', 'direccion', 'rol')}),
    )
    list_display = ('username', 'email', 'rol', 'fecha_registro')
    readonly_fields = ('fecha_registro',)  # opcional: para verlo en detalle como solo lectura

admin.site.register(Usuario, UsuarioAdmin)