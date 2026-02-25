from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app.models import Vehiculo
from app.forms import VehiculoForm



class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'vehiculo/listar.html'
    context_object_name = 'vehiculo'

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de vehiculo'
        context['crear_url'] = reverse_lazy('app:crear_vehiculo')
        return context

class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculo')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear vehiculo'
        context['listar_url'] = reverse_lazy('app:listar_vehiculo')
        return context



class VehiculoUpdateView(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculo')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar vehiculo'
        context['listar_url'] = reverse_lazy('app:listar_vehiculo')
        return context



class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    template_name = 'vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_vehiculo')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar vehiculo'
        context['listar_url'] = reverse_lazy('app:listar_vehiculo')
        return context