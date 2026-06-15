from django.urls import path
from . import views

app_name = 'multas'
urlpatterns = [
    path('', views.MultaListView.as_view(), name='list'),
    path('pagar/<int:pk>/', views.MultaPagarView.as_view(), name='pagar'),
]