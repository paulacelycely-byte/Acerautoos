from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from app.models import Cliente
from app.forms import ClienteForm

# MIXIN PERSONALIZADO PARA ADMINISTRADORES
class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        # Solo permite el paso si el cargo es ADMIN o es superusuario
        return self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder al módulo de clientes.")
        # Redirigimos al dashboard o inicio para evitar un bucle si se intenta entrar a la lista
        return redirect('app:dashboard') 

# 1. LISTADO DE CLIENTES (Restringido para mecánicos)
class ClienteListView(LoginRequiredMixin, SoloAdminMixin, ListView):
    model = Cliente
    template_name = 'cliente/listar.html'
    context_object_name = 'clientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Clientes'
        return context

# 2. CREAR CLIENTE (Solo Admin)
class ClienteCreateView(LoginRequiredMixin, SoloAdminMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear.html'
    success_url = reverse_lazy('app:listar_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Registrar Nuevo Cliente'
        context['es_editar'] = False
        context['next']       = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Cliente registrado con éxito en Acerautos.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:crear_vehiculo'))
        return redirect(self.success_url)

# 3. EDITAR CLIENTE (Solo Admin)
class ClienteUpdateView(LoginRequiredMixin, SoloAdminMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear.html'
    success_url = reverse_lazy('app:listar_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Editar Datos del Cliente'
        context['es_editar'] = True
        context['next']       = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Datos del cliente actualizados correctamente.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)

# 4. ELIMINAR CLIENTE (Solo Admin)
class ClienteDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
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