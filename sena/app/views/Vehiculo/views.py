from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from app.models import Vehiculo
from app.forms import VehiculoForm

class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'vehiculo/listar.html'
    context_object_name = 'vehiculos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Esto llena el título en el listado
        context['titulo'] = 'Listado de Vehículos'
        return context

class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Esto es lo que faltaba para que se vea el título en "Crear"
        context['titulo'] = 'Registrar Nuevo Vehículo'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Vehículo registrado con éxito.')
        return super().form_valid(form)

class VehiculoUpdateView(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Esto es lo que faltaba para que se vea el título en "Editar"
        context['titulo'] = 'Editar Vehículo'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Vehículo actualizado correctamente.')
        return super().form_valid(form)

class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    template_name = 'vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Vehículo'
        return context

    def post(self, request, *args, **kwargs):
        # Mantenemos tu lógica de mensajes para la eliminación
        messages.success(self.request, 'Vehículo eliminado del sistema.')
        return super().post(request, *args, **kwargs)