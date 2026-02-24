from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from app.models import Usuario
from app.forms import UsuarioForm




class UsuarioListView(ListView):
    model = Usuario
    template_name = 'Usuario/listar.html'
    context_object_name = 'Usuario'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Usuarios'
        context['crear_url'] = reverse_lazy('app:crear_Usuario')
        return context


class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Usuario/crear.html'
    success_url = reverse_lazy('app:listar_Usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Usuario'
        context['listar_url'] = reverse_lazy('app:listar_Usuario')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se creó una venta")
        return super().form_valid(form)

    
class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Usuario/crear.html'
    success_url = reverse_lazy('app:listar_Usuario')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_Usuario')
        return context


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'Usuario/eliminar.html'
    success_url = reverse_lazy('app:listar_Usuario')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_Usuario')
        return context
    
