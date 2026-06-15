from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios.views import LoginView, LogoutView, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usuarios/', include('apps.usuarios.urls')),
    path('libros/', include('apps.libros.urls')),
    path('prestamos/', include('apps.prestamos.urls')),
    path('multas/', include('apps.multas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)