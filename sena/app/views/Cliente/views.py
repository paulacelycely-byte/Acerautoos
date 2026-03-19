from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from app.models import Cliente
from app.forms import ClienteForm

# 1. LISTADO DE CLIENTES
class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente/listar.html'
    context_object_name = 'clientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Clientes'
        return context

# 2. CREAR CLIENTE
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear.html'
    success_url = reverse_lazy('app:listar_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Registrar Nuevo Cliente'
        context['es_editar'] = False
        context['next']      = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Cliente registrado con éxito en Acerautos.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:crear_vehiculo'))
        return redirect(self.success_url)

# 3. EDITAR CLIENTE
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear.html'
    success_url = reverse_lazy('app:listar_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Editar Datos del Cliente'
        context['es_editar'] = True
        context['next']      = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Datos del cliente actualizados correctamente.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)

# 4. ELIMINAR CLIENTE
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cliente/eliminar.html'
    success_url = reverse_lazy('app:listar_clientes')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'El cliente ha sido eliminado del sistema.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Cliente'
        return context