from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from app.models import OrdenServicio
from app.forms import OrdenServicioForm   # 👈 Asegúrate que tu form se llame así


# ==============================
# LISTAR
# ==============================
class OrdenServicioListView(ListView):
    model = OrdenServicio
    template_name = 'Servicio/listar.html'
    context_object_name = 'servicio'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Órdenes de Servicio'
        context['crear_url'] = reverse_lazy('app:crear_servicio')
        return context


# ==============================
# CREAR
# ==============================
class OrdenServicioCreateView(CreateView):
    model = OrdenServicio
    form_class = OrdenServicioForm
    template_name = 'Servicio/crear.html'
    success_url = reverse_lazy('app:orden_servicio_list')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Orden de Servicio'
        context['listar_url'] = reverse_lazy('app:orden_servicio_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Se creó una nueva orden de servicio')
        return super().form_valid(form)


# ==============================
# EDITAR
# ==============================
class OrdenServicioUpdateView(UpdateView):
    model = OrdenServicio
    form_class = OrdenServicioForm
    template_name = 'Servicio/crear.html'
    success_url = reverse_lazy('app:orden_servicio_list')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Orden de Servicio'
        context['listar_url'] = reverse_lazy('app:listar_servicio')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Se actualizó la orden de servicio')
        return super().form_valid(form)


# ==============================
# ELIMINAR
# ==============================
class OrdenServicioDeleteView(DeleteView):
    model = OrdenServicio
    template_name = 'Servicio/eliminar.html'
    success_url = reverse_lazy('app:orden_servicio_list')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Orden de Servicio'
        context['listar_url'] = reverse_lazy('app:orden_servicio_list')
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Se eliminó la orden de servicio')
        return super().delete(request, *args, **kwargs)