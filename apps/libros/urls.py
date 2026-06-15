from django.urls import path
from . import views

app_name = 'libros'
urlpatterns = [
    # Libros
    path('', views.LibroListView.as_view(), name='list'),
    path('<int:pk>/', views.LibroDetailView.as_view(), name='detail'),
    path('crear/', views.LibroCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', views.LibroUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', views.LibroDeleteView.as_view(), name='delete'),
    
    # Ejemplares (anidadas a libro)
    path('libro/<int:libro_id>/ejemplares/crear/', views.EjemplarCreateView.as_view(), name='ejemplar_create'),
    path('ejemplares/', views.EjemplarListView.as_view(), name='ejemplar_list'),
    path('ejemplares/editar/<int:pk>/', views.EjemplarUpdateView.as_view(), name='ejemplar_update'),
    path('ejemplares/eliminar/<int:pk>/', views.EjemplarDeleteView.as_view(), name='ejemplar_delete'),
    
    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/eliminar/<int:pk>/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
]