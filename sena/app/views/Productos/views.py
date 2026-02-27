from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from app.models import Productos
from app.forms import ProductosForm


class ProductosListView(ListView):
    model = Productos
    template_name = 'productos/listar.html'
    context_object_name = 'productos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de productos'
        context['crear_url'] = reverse_lazy('app:crear_productos')
        return context


class ProductosCreateView(CreateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/crear.html'
    success_url = reverse_lazy('app:listar_productos')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Producto creado correctamente')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear productos'
        context['listar_url'] = reverse_lazy('app:listar_productos')
        return context


class ProductosUpdateView(UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/crear.html'
    success_url = reverse_lazy('app:listar_productos')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado correctamente')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Productos'
        context['listar_url'] = reverse_lazy('app:listar_productos')
        return context


class ProductosDeleteView(DeleteView):
    model = Productos
    template_name = 'productos/eliminar.html'
    success_url = reverse_lazy('app:listar_productos')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Producto eliminado correctamente')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar productos'
        context['listar_url'] = reverse_lazy('app:listar_productos')
        return context