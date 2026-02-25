from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # El candado
from app.models import Categorias
from app.forms import CategoriaForm

# --- LISTAR ---
class categoriaListView(LoginRequiredMixin, ListView): # Mixin agregado
    model = Categorias
    template_name = 'categoria/listar.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Categorías'
        context['crear_url'] = reverse_lazy('app:crear_categoria')
        return context

# --- CREAR ---
class CategoriaCreateView(LoginRequiredMixin, CreateView): # Mixin agregado
    model = Categorias
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('app:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Categoría'
        context['listar_url'] = reverse_lazy('app:listar_categoria')
        return context

# --- EDITAR ---
class CategoriaUpdateView(LoginRequiredMixin, UpdateView): # Mixin agregado
    model = Categorias
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('app:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Categoría'
        context['listar_url'] = reverse_lazy('app:listar_categoria')
        return context

# --- ELIMINAR ---
class CategoriaDeleteView(LoginRequiredMixin, DeleteView): # Mixin agregado
    model = Categorias
    template_name = 'categoria/eliminar.html'
    success_url = reverse_lazy('app:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categoría'
        context['listar_url'] = reverse_lazy('app:listar_categoria')
        return context