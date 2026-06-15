from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.UsuarioListView.as_view(), name='list'),
    path('crear/', views.UsuarioCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', views.UsuarioDeleteView.as_view(), name='delete'),
]