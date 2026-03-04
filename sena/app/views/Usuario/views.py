from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # Opcional: para que solo logueados entren

# Importación absoluta desde la raíz de la app
from app.models import Usuario 
from app.forms import UsuarioForm

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'Usuario/listar.html'
    context_object_name = 'usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Usuarios'
        context['crear_url'] = reverse_lazy('app:crear_usuario')
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        return context

class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Usuario/crear.html'
    success_url = reverse_lazy('app:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        context['action'] = 'add'
        return context

class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Usuario/crear.html'
    success_url = reverse_lazy('app:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        context['action'] = 'edit'
        return context

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'Usuario/eliminar.html'
    success_url = reverse_lazy('app:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        return context