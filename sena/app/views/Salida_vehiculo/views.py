from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app.models import Salida_Vehiculo
from app.forms import Salida_VehiculoForm
from django.contrib import messages

class Salida_VehiculoListView(ListView):
    model = Salida_Vehiculo
    template_name = 'Salida_vehiculo/listar.html'
    context_object_name = 'Salida_vehiculo'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Salidas de Vehículos'
        context['crear_url'] = reverse_lazy('app:crear_salida_vehiculo')
        return context


class Salida_VehiculoCreateView(CreateView):
    model = Salida_Vehiculo
    form_class = Salida_VehiculoForm
    template_name = 'Salida_vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_salida_vehiculo')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Salida de Vehículo'
        context['listar_url'] = reverse_lazy('app:listar_salida_vehiculo')
        return context
    def form_valid(self, form):
        messages.success(self.request,'Se creo una nueva salida de vehículo')
        return super().form_valid(form)
    


class Salida_VehiculoUpdateView(UpdateView):
    model = Salida_Vehiculo
    form_class = Salida_VehiculoForm
    template_name = 'Salida_vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_salida_vehiculo')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Salida de Vehículo'
        context['listar_url'] = reverse_lazy('app:listar_salida_vehiculo')
        return context


class Salida_VehiculoDeleteView(DeleteView):
    model = Salida_Vehiculo
    template_name = 'Salida_vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_salida_vehiculo')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Salida de Vehículo'
        context['listar_url'] = reverse_lazy('app:listar_salida_vehiculo')
        return context
