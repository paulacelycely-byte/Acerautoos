from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# IMPORTACIÓN ABSOLUTA (Soluciona el error de la imagen 1)
from app.models import Proveedor
from app.forms import ProveedorForm

class ProveedorListView(ListView):
    model = Proveedor
    # AJUSTADO A TU CARPETA SINGULAR (Soluciona el error de las imágenes 2 y 3)
    template_name = 'Proveedor/listar.html' 
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Proveedores'
        context['crear_url'] = reverse_lazy('app:crear_proveedor')
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context

class ProveedorCreateView(SuccessMessageMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = 'Proveedor creado exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        context['action'] = 'add'
        return context

class ProveedorUpdateView(SuccessMessageMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Proveedor/crear.html' 
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = 'Proveedor actualizado exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        context['action'] = 'edit'
        return context

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'Proveedor/eliminar.html'
    success_url = reverse_lazy('app:listar_proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Proveedor eliminado exitosamente.')
        return self.delete(request, *args, **kwargs)