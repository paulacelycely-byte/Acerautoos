from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from app.models import Notificacion
from app.forms import NotificacionForm


class NotificacionListView(ListView):
    model = Notificacion
    template_name = 'notificacion/listar.html'
    context_object_name = 'notificaciones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de notificaciones'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        return context


class NotificacionCreateView(CreateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        return context


class NotificacionUpdateView(UpdateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        return context


class NotificacionDeleteView(DeleteView):
    model = Notificacion
    template_name = 'notificacion/eliminar.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        return context
