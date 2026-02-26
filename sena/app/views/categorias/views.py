from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app.views.categorias.views import *
from app.views import *

from app.models import Categoria
from app.forms import CategoriaForm



class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/listar.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Categorías'
        context['crear_url'] = reverse_lazy('app:crear_categorias')
        return context

from django.urls import reverse_lazy
from django.contrib import messages

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'Categorias/crear.html'
    success_url = reverse_lazy('app:listar_categoria')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría guardada correctamente')
        return super().form_valid(form)


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('app:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Categorías'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        return context



class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'categoria/eliminar.html'
    success_url = reverse_lazy('app:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categorías'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        return context
