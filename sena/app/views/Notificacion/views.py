from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.models import Notificacion
from app.forms import NotificacionForm


class NotificacionListView(ListView):
    model = Notificacion
    template_name = 'Notificacion/listar.html'
    context_object_name = 'object_list'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Notificaciones'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        return context


class NotificacionCreateView(CreateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Notificación"
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se creó correctamente la notificación")
        return super().form_valid(form)


class NotificacionUpdateView(UpdateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se editó correctamente")
        return super().form_valid(form)


class NotificacionDeleteView(DeleteView):
    model = Notificacion
    template_name = 'Notificacion/eliminar.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se eliminó correctamente")
        return super().form_valid(form)