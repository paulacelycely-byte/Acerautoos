from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app.models import Servicio
from app.forms import ServicioForm
from django.contrib import messages


class ServicioListView(ListView):
    model = Servicio
    template_name = 'Servicio/listar.html'
    context_object_name = 'servicio'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Servicios'
        context['crear_url'] = reverse_lazy('app:crear_servicio')
        return context


class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'Servicio/crear.html'
    success_url = reverse_lazy('app:listar_servicio')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Servicio'
        context['listar_url'] = reverse_lazy('app:listar_servicio')
        return context
    
    #mensajes de confirmacion
    def form_valid(self, form):
        messages.success(self.request,'Se creo un nuevo servicio')
        return super().form_valid(form)


class ServicioUpdateView(UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'Servicio/crear.html'
    success_url = reverse_lazy('app:listar_servicio')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Servicio'
        context['listar_url'] = reverse_lazy('app:listar_servicio')
        return context
    
    #mensajes de confirmacion
    def form_valid(self, form):
        messages.success(self.request,'Se actualizó un servicio')
        return super().form_valid(form)


class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'Servicio/eliminar.html'
    success_url = reverse_lazy('app:listar_servicio')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Servicio'
        context['listar_url'] = reverse_lazy('app:listar_servicio')
        return context
    
#mensajes de confirmacion
    def form_valid(self, form):
        messages.success(self.request,'Se eliminó un servicio')
        return super().form_valid(form)
