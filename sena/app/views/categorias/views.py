from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app.models import Categorias
from app.forms import CategoriaForm



class categoriaListView(ListView):
    model = Categorias
    template_name = 'categoria/listar.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Categorías'
        context['crear_url'] = reverse_lazy('app:crear_categoria')
        return context

from django.urls import reverse_lazy
from django.contrib import messages

class CategoriaCreateView(CreateView):
    model = Categorias
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('app:listar_categoria')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría guardada correctamente')
        return super().form_valid(form)


class CategoriaUpdateView(UpdateView):
    model = Categorias
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('app:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Categoría'
        context['listar_url'] = reverse_lazy('app:listar_categoria')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Se edito correctamente")
        return super().form_valid(form)



class CategoriaDeleteView(DeleteView):
    model = Categorias
    template_name = 'categoria/eliminar.html'
    success_url = reverse_lazy('app:listar_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categoría'
        context['listar_url'] = reverse_lazy('app:listar_categoria')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Se elimino correctamente")
        return super().form_valid(form)
