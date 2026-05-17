from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum

from app.models import DetalleOrdenProducto
from app.forms import DetalleOrdenProductoForm


# ── MIXINS ────────────────────────────────────────────────────────────

class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser
        )
    def handle_no_permission(self):
        messages.error(self.request, "Acceso denegado: Se requieren permisos de administrador.")
        return redirect('app:detalle_orden_list')


class AccesoLecturaTallerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.cargo is not None
    def handle_no_permission(self):
        messages.error(self.request, "Debes ser parte del personal de Acerautos para ver esto.")
        return redirect('app:dashboard')


# ── 1. LISTADO ────────────────────────────────────────────────────────

class DetalleOrdenListView(LoginRequiredMixin, AccesoLecturaTallerMixin, ListView):
    model = DetalleOrdenProducto
    template_name = 'detalle/detalle_orden_list.html'
    context_object_name = 'detalles'

    def get_queryset(self):
        return DetalleOrdenProducto.objects.select_related(
            'orden__vehiculo__marca',
            'producto__marca',
        ).order_by('-orden__id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        total_registros = qs.count()
        total_ordenes   = qs.values('orden').distinct().count()
        total_unidades  = qs.aggregate(t=Sum('cantidad'))['t'] or 0

        # Total correcto: suma de (cantidad × precio) por cada registro
        total_general = sum(d.cantidad * d.producto.precio for d in qs)

        context.update({
            'titulo':          'Historial de Productos',
            'total_registros': total_registros,
            'total_ordenes':   total_ordenes,
            'total_unidades':  total_unidades,
            'total_general':   total_general,
        })
        return context


# ── 2. CREAR ─────────────────────────────────────────────────────────

class DetalleOrdenCreateView(LoginRequiredMixin, SoloAdminMixin, CreateView):
    model = DetalleOrdenProducto
    form_class = DetalleOrdenProductoForm
    template_name = 'detalle/detalle_orden_add.html'
    success_url = reverse_lazy('app:detalle_orden_list')

    def form_valid(self, form):
        try:
            form.instance.full_clean()
            messages.success(self.request, "Producto registrado correctamente.")
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


# ── 3. EDITAR ────────────────────────────────────────────────────────

class DetalleOrdenUpdateView(LoginRequiredMixin, SoloAdminMixin, UpdateView):
    model = DetalleOrdenProducto
    form_class = DetalleOrdenProductoForm
    template_name = 'detalle/detalle_orden_add.html'
    success_url = reverse_lazy('app:detalle_orden_list')


# ── 4. ELIMINAR ──────────────────────────────────────────────────────

class DetalleOrdenDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
    model = DetalleOrdenProducto
    template_name = 'detalle/detalle_orden_confirm_delete.html'
    success_url = reverse_lazy('app:detalle_orden_list')