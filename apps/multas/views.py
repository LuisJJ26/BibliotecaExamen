from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.mixins import BibliotecarioRequiredMixin
from .models import Multa
from django.shortcuts import redirect

class MultaListView(LoginRequiredMixin, ListView):
    model = Multa
    template_name = 'multas/multa_list.html'
    context_object_name = 'multas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol == 'usuario':
            queryset = queryset.filter(usuario=self.request.user)
        pagada = self.request.GET.get('pagada')
        if pagada is not None:
            queryset = queryset.filter(pagada=(pagada == '1'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_admin'] = self.request.user.rol in ['administrador', 'bibliotecario']
        return context

class MultaPagarView(BibliotecarioRequiredMixin, UpdateView):
    model = Multa
    fields = []
    template_name = 'multas/multa_confirm_pagar.html'
    success_url = reverse_lazy('multas:list')

    def post(self, request, *args, **kwargs):
        multa = self.get_object()
        multa.marcar_pagada()
        messages.success(request, 'Multa marcada como pagada.')
        return redirect('multas:list')