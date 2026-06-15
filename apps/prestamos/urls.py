from django.urls import path
from . import views

app_name = 'prestamos'
urlpatterns = [
    path('', views.PrestamoListView.as_view(), name='list'),
    path('crear/', views.PrestamoCreateView.as_view(), name='create'),
    path('devolver/<int:pk>/', views.PrestamoDevolverView.as_view(), name='devolver'),
    path('renovar/<int:pk>/', views.PrestamoRenovarView.as_view(), name='renovar'),
    path('buscar-usuarios/', views.buscar_usuarios_ajax, name='buscar_usuarios'),
    path('buscar-ejemplares/', views.buscar_ejemplares_ajax, name='buscar_ejemplares'),
]