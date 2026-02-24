from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from app.models import Entrada_vehiculo
from app.forms import Entrada_vehiculoForm
from app.models import Ventas
from app.forms import VentasForm




class Entrada_vehiculoListView(ListView):
    model = Entrada_vehiculo
    template_name = 'Entrada_vehiculo/listar.html'
    context_object_name = 'Entrada_vehiculo'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Entradas de Vehículos'
        context['crear_url'] = reverse_lazy('app:crear_entrada_vehiculo')
        return context


class Entrada_vehiculoCreateViews(CreateView):
    model = Entrada_vehiculo
    form_class = Entrada_vehiculoForm
    template_name = 'Entrada_vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_entrada_vehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Entrada de vehiculo'
        context['listar_url'] = reverse_lazy('app:listar_entrada_vehiculo')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se creó un nuevo ingreso")
        return super().form_valid(form)

    
class Entrada_vehiculoUpdateView(UpdateView):
    model = Entrada_vehiculo
    form_class = Entrada_vehiculoForm
    template_name = 'Entrada_vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_entrada_vehiculo')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Entrada de Vehículo'
        context['listar_url'] = reverse_lazy('app:listar_entrada_vehiculo')
        return context


class EntradaVehiculoDeleteView(DeleteView):
    model = Entrada_vehiculo
    template_name = 'Entrada_vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_entrada_vehiculo')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Entrada de Vehículo'
        context['listar_url'] = reverse_lazy('app:listar_entrada_vehiculo')
        return context
    
