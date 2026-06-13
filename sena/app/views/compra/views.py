from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone

from ...models import Compra, Caja, Factura
from ...forms import CompraForm


# ── Solo ADMIN — todo este módulo es restringido ─────────────────
class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos de administrador para gestionar las compras.")
        return redirect('app:dashboard')


# ── LISTAR — Solo Admin ───────────────────────────────────────────
class CompraListView(LoginRequiredMixin, SoloAdminMixin, ListView):
    model = Compra
    template_name = 'Compra/listar.html'
    context_object_name = 'compras'

    def get_queryset(self):
        return Compra.objects.all().order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Historial de Compras'
        return context


# ── CREAR — Solo Admin ────────────────────────────────────────────
class CompraCreateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'Compra/crear.html'
    success_url = reverse_lazy('app:lista_compras')
    success_message = "Compra registrada correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nueva Compra'
        return context

    def form_valid(self, form):
        compra = form.save(commit=False)
        compra.producto.stock += compra.cantidad
        compra.producto.save(update_fields=['stock'])
        compra.save()
        return super().form_valid(form)


# ── EDITAR — Solo Admin ───────────────────────────────────────────
class CompraUpdateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'Compra/crear.html'
    success_url = reverse_lazy('app:lista_compras')
    success_message = "Compra modificada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Registro de Compra'
        return context

    def form_valid(self, form):
        compra_anterior = Compra.objects.get(pk=self.object.pk)
        compra = form.save(commit=False)

        if compra_anterior.producto_id != compra.producto_id:
            compra_anterior.producto.stock -= compra_anterior.cantidad
            compra_anterior.producto.save(update_fields=['stock'])
            compra.producto.stock += compra.cantidad
            compra.producto.save(update_fields=['stock'])
        else:
            diferencia = compra.cantidad - compra_anterior.cantidad
            compra.producto.stock += diferencia
            compra.producto.save(update_fields=['stock'])

        compra.save()
        return super().form_valid(form)


# ── ELIMINAR — Solo Admin ─────────────────────────────────────────
class CompraDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
    model = Compra
    template_name = 'Compra/eliminar.html'
    success_url = reverse_lazy('app:lista_compras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Registro de Compra'
        return context

    def form_valid(self, form):
        compra = self.get_object()
        compra.producto.stock -= compra.cantidad
        if compra.producto.stock < 0:
            compra.producto.stock = 0
        compra.producto.save(update_fields=['stock'])
        messages.success(self.request, "El registro de compra ha sido eliminado.")
        return super().form_valid(form)


# ── PAGAR — Solo Admin ────────────────────────────────────────────
class PagarCompraView(LoginRequiredMixin, SoloAdminMixin, View):
    def post(self, request, pk):
        compra = get_object_or_404(Compra, pk=pk)

        if compra.estado_pago == 'Pagada':
            messages.warning(request, "Esta compra ya fue pagada.")
            return redirect('app:lista_compras')

        metodo = request.POST.get('metodo_pago')
        if not metodo:
            messages.error(request, "Seleccione un método de pago.")
            return redirect('app:lista_compras')

        compra.estado_pago = 'Pagada'
        compra.metodo_pago = metodo
        compra.fecha_pago  = timezone.now()
        compra.save()

        Caja.objects.create(
            descripcion = f"Compra Factura {compra.num_factura_proveedor}",
            monto       = compra.total_pagado,
            tipo        = 'EGRESO',
            categoria   = 'Proveedores',
            metodo_pago = metodo,
        )

        try:
            factura = compra.factura
            factura.estado_pago = 'Pagada'
            factura.metodo_pago = metodo
            factura.save()
        except Factura.DoesNotExist:
            pass

        messages.success(request, f"Compra {compra.num_factura_proveedor} pagada correctamente.")
        return redirect('app:lista_compras')