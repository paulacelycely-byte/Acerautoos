from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.models import Ventas 
from app.forms import VentasForm

class VentasListView(ListView):
    model = Ventas
    template_name = 'Ventas/listar.html'
    context_object_name = 'Ventas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        context['crear_url'] = reverse_lazy('app:crear_Ventas')
        return context

class VentasCreateView(CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'Ventas/crear.html'
    success_url = reverse_lazy('app:listar_Ventas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Ventas"
        context['listar_url'] = reverse_lazy('app:listar_Ventas')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Llamamos al método de calcular_total que definimos en el Modelo
        self.object.calcular_total() 
        messages.success(self.request, "Venta registrada con éxito")
        return response

class VentasUpdateView(UpdateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'Ventas/crear.html'
    success_url = reverse_lazy('app:listar_Ventas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Venta'
        context['listar_url'] = reverse_lazy('app:listar_Ventas')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.calcular_total()
        messages.success(self.request, "Venta actualizada")
        return response

class Ventas_delete(DeleteView):
    model = Ventas
    template_name = 'Ventas/eliminar.html'
    success_url = reverse_lazy('app:listar_Ventas')