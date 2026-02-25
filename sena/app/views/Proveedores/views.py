from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin 
from ...models import Proveedor
from ...forms import ProveedorForm
from django.contrib.auth.mixins import LoginRequiredMixin

# LISTAR
class ProveedorListView(LoginRequiredMixin, ListView): # Mixin agregado
    model = Proveedor
    template_name = 'Prooveedores/listar.html'
    context_object_name = 'object_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Proveedores'
        context['crear_url'] = reverse_lazy('app:crear_proveedor')
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context

# CREAR
class ProveedorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView): # Mixin agregado al inicio
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Prooveedores/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = ' Proveedor creado exitosamente'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Error al guardar. Por favor verifica los campos')
        return super().form_invalid(form)

# EDITAR
class ProveedorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView): # Mixin agregado al inicio
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Prooveedores/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = '✅ Proveedor actualizado exitosamente'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Error al actualizar. Por favor verifica los campos')
        return super().form_invalid(form)

# ELIMINAR
class ProveedorDeleteView(LoginRequiredMixin, DeleteView): # Mixin agregado
    model = Proveedor
    template_name = 'Prooveedores/eliminar.html'
    success_url = reverse_lazy('app:listar_proveedores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, '🗑️ Proveedor eliminado exitosamente')
        return self.delete(request, *args, **kwargs)