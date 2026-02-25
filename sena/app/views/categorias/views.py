from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app.views.Categorias.views import *
from app.views import *

from app.models import Categorias
from app.forms import CategoriasForm



class CategoriasListView(ListView):
    model = Categorias
    template_name = 'categorias/listar.html'
    context_object_name = 'categorias'

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Categorías'
        context['crear_url'] = reverse_lazy('app:crear_categorias')
        return context

class CategoriasCreateView(CreateView):
    model = Categorias
    form_class = CategoriasForm
    template_name = 'categorias/crear.html'
    success_url = reverse_lazy('app:listar_categorias')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Categorías'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        return context



class CategoriasUpdateView(UpdateView):
    model = Categorias
    form_class = CategoriasForm
    template_name = 'categorias/crear.html'
    success_url = reverse_lazy('app:listar_categorias')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Categorías'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        return context



class CategoriasDeleteView(DeleteView):
    model = Categorias
    template_name = 'categorias/eliminar.html'
    success_url = reverse_lazy('app:listar_categorias')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categorías'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        return context
