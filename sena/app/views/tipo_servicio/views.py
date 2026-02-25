from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.models import tipo_servicio
from app.forms import TipoServicioForm
from django.contrib.auth.mixins import LoginRequiredMixin

class TipoServicioListView(LoginRequiredMixin, ListView): # Mixin agregado
    model = tipo_servicio
    template_name = 'TipoServicio/listar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Tipos de Servicio'
        context['crear_url'] = reverse_lazy('app:crear_servicio')
        return context

class TipoServicioCreateView(LoginRequiredMixin, CreateView): # Mixin agregado
    model = tipo_servicio
    form_class = TipoServicioForm
    template_name = 'TipoServicio/crear.html'
    success_url = reverse_lazy('app:listar_servicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tipo de Servicio'
        context['listar_url'] = reverse_lazy('app:listar_servicio')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, ' Tipo de servicio creado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, ' Error al guardar. Por favor verifica los campos')
        return super().form_invalid(form)

class TipoServicioUpdateView(LoginRequiredMixin, UpdateView): # Mixin agregado
    model = tipo_servicio
    form_class = TipoServicioForm
    template_name = 'TipoServicio/editar.html'
    success_url = reverse_lazy('app:listar_servicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Servicio'
        context['listar_url'] = reverse_lazy('app:listar_servicio')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, ' Tipo de servicio actualizado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, ' Error al actualizar. Por favor verifica los campos')
        return super().form_invalid(form)

class TipoServicioDeleteView(LoginRequiredMixin, DeleteView): # Mixin agregado
    model = tipo_servicio
    template_name = 'TipoServicio/eliminar.html'
    success_url = reverse_lazy('app:listar_servicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tipo de Servicio'
        context['listar_url'] = reverse_lazy('app:listar_servicio')
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, ' Tipo de servicio eliminado exitosamente')
        return super().delete(request, *args, **kwargs)