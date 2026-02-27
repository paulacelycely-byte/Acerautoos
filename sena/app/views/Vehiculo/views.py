from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from app.models import Vehiculo
from app.forms import VehiculoForm

# Decorador para todas las vistas basadas en clases
class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'vehiculo/listar.html'
    context_object_name = 'vehiculo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de vehículo'
        context['crear_url'] = reverse_lazy('app:crear_vehiculo')
        return context



class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear vehículo'
        context['listar_url'] = reverse_lazy('app:listar_vehiculo')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El vehículo se guardó correctamente')
        return super().form_valid(form)



class VehiculoUpdateView(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar vehículo'
        context['listar_url'] = reverse_lazy('app:listar_vehiculo')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El vehículo se actualizó correctamente')
        return super().form_valid(form)


class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    template_name = 'vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_vehiculo')

    def delete(self, request, *args, **kwargs):
        # Aquí el mensaje se guardará y se mostrará con SweetAlert2 después
        messages.success(self.request, 'El vehículo se eliminó correctamente')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar vehículo'
        context['listar_url'] = reverse_lazy('app:listar_vehiculo')
        return context