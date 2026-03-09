from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal

from app.models import Factura, OrdenServicio, Producto
from app.forms import FacturaForm


# ─── LISTAR ───────────────────────────────────────────────
class FacturaListView(ListView):
    model = Factura
    template_name = 'factura/listar.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Facturas'
        return context


# ─── CREAR ────────────────────────────────────────────────
class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'factura/crear.html'
    success_url = reverse_lazy('app:listar_factura')

    def form_valid(self, form):
        factura = form.save(commit=False)
        tipo = factura.tipo

        if tipo == 'SERVICIO':
            orden = factura.orden_servicio
            subtotal = orden.servicio.precio_mano_obra
            for detalle in orden.productos_usados.select_related('producto').all():
                subtotal += detalle.producto.precio * detalle.cantidad
            factura.subtotal = subtotal

        elif tipo == 'PRODUCTO':
            factura.subtotal = factura.producto.precio * factura.cantidad
            factura.producto.stock -= factura.cantidad
            factura.producto.save()

        factura.iva = factura.subtotal * Decimal('0.19')
        factura.total = factura.subtotal + factura.iva
        factura.estado_pago = 'Pendiente'
        factura.save()

        messages.success(self.request, f"Factura {factura.numero_factura} creada correctamente.")
        return super().form_valid(form)


# ─── DETALLE ──────────────────────────────────────────────
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'factura/detalle.html'
    context_object_name = 'factura'


# ─── ELIMINAR ─────────────────────────────────────────────
class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'factura/eliminar.html'
    success_url = reverse_lazy('app:listar_factura')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Factura'
        return context


# ─── PAGAR (POST) ─────────────────────────────────────────
class PagarFacturaView(View):
    def post(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)
        metodo = request.POST.get('metodo_pago', '').strip()

        metodos_validos = [m[0] for m in Factura.METODOS_PAGO]
        if not metodo or metodo not in metodos_validos:
            messages.error(request, "Seleccione un método de pago válido.")
        elif factura.estado_pago == 'Pagada':
            messages.warning(request, "Esta factura ya fue pagada.")
        else:
            factura.metodo_pago = metodo
            factura.estado_pago = 'Pagada'
            factura.fecha_pago = timezone.now()
            factura.save()
            messages.success(request, f"Pago registrado con {factura.get_metodo_pago_display()}.")

        return redirect('app:listar_factura')