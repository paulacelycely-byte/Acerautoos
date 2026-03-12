from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Sum

from app.models import Caja
from app.forms import CajaForm


class CajaListView(ListView):
    model = Caja
    template_name = 'Caja/listar.html'
    context_object_name = 'object_list'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Caja.objects.all().order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Movimientos de Caja'
        context['crear_url'] = reverse_lazy('app:caja_crear')

        qs = self.get_queryset()
        total_ingresos = qs.filter(tipo='INGRESO').aggregate(t=Sum('monto'))['t'] or 0
        total_egresos  = qs.filter(tipo='EGRESO').aggregate(t=Sum('monto'))['t'] or 0
        context['total_ingresos'] = total_ingresos
        context['total_egresos']  = total_egresos
        context['saldo_caja']     = total_ingresos - total_egresos
        return context


class CajaCreateView(CreateView):
    model = Caja
    form_class = CajaForm
    template_name = 'Caja/crear.html'
    success_url = reverse_lazy('app:caja_listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Movimiento de Caja"
        context['listar_url'] = reverse_lazy('app:caja_listar')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se registró correctamente el movimiento")
        return super().form_valid(form)


class CajaUpdateView(UpdateView):
    model = Caja
    form_class = CajaForm
    template_name = 'Caja/crear.html'
    success_url = reverse_lazy('app:caja_listar')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Movimiento de Caja'
        context['listar_url'] = reverse_lazy('app:caja_listar')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se editó correctamente el movimiento")
        return super().form_valid(form)


class CajaDeleteView(DeleteView):
    model = Caja
    template_name = 'Caja/eliminar.html'
    success_url = reverse_lazy('app:caja_listar')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Movimiento de Caja'
        context['listar_url'] = reverse_lazy('app:caja_listar')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se eliminó correctamente el movimiento")
        return super().form_valid(form)