from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError
from app.models import TipoServicio
from app.forms import TipoServicioForm


class TipoServicioListView(ListView): 
    model = TipoServicio
    template_name = 'TipoServicio/listar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Tipos de Servicio'
        context['crear_url'] = reverse_lazy('app:tipo_servicio_create') 
        return context

class TipoServicioCreateView(CreateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'TipoServicio/crear.html'
    success_url = reverse_lazy('app:tipo_servicio_list') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tipo de Servicio'
        context['listar_url'] = reverse_lazy('app:tipo_servicio_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de servicio creado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al guardar. Por favor verifica los campos')
        return super().form_invalid(form)

class TipoServicioUpdateView(UpdateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'TipoServicio/crear.html'
    success_url = reverse_lazy('app:tipo_servicio_list') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Servicio'
        context['listar_url'] = reverse_lazy('app:tipo_servicio_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de servicio actualizado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar. Por favor verifica los campos')
        return super().form_invalid(form)

class TipoServicioDeleteView(DeleteView):
    model = TipoServicio
    template_name = 'TipoServicio/eliminar.html'
    success_url = reverse_lazy('app:tipo_servicio_list') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tipo de Servicio'
        context['listar_url'] = reverse_lazy('app:tipo_servicio_list')
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            nombre = self.object.nombre
            self.object.delete()
            messages.success(request, f'El servicio "{nombre}" fue eliminado exitosamente.')
            return redirect(self.success_url)
        except ProtectedError:
            nombre = self.get_object().nombre
            messages.error(
                request,
                f'No se puede eliminar "{nombre}" porque tiene órdenes de servicio asociadas. '
                f'Elimina primero esas órdenes e intenta de nuevo.'
            )
            return redirect('app:tipo_servicio_list')