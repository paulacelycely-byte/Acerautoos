from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from app.models import Entrada_vehiculo
from app.forms import Entrada_vehiculoForm
from app.models import Ventas
from app.forms import VentasForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView


class VentasListView(ListView):
    model = Ventas
    template_name = 'Ventas/listar.html'
    context_object_name = 'Ventas'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        context['crear_url'] = reverse_lazy('app:crear_Ventas')
        return context


class VentasCreateView(CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'Ventas/crear.html'
    success_url = reverse_lazy('app:listar_Ventas')

    # @method_decorator(login_required)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Ventas"
        context['listar_url'] = reverse_lazy('app:listar_Ventas')
        return context


    def form_valid(self, form):
        messages.success(self.request,"Se creo un nuevo ingreso")
        return super().form_valid(form)


class VentasUpdateView(UpdateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'Ventas/crear.html'
    success_url = reverse_lazy('app:listar_Ventas')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Venta'
        context['listar_url'] = reverse_lazy('app:listar_Ventas')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se edito correctamente")
        return super().form_valid(form)


class Ventas_delete(DeleteView):
    model = Ventas
    template_name = 'Ventas/eliminar.html'
    success_url = reverse_lazy('app:listar_Ventas')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Venta'
        context['listar_url'] = reverse_lazy('app:listar_Ventas')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se elimino correctamente")
        return super().form_valid(form)
