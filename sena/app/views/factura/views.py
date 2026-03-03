from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from app.models import Factura
from app.forms import FacturaForm
from django.contrib import messages
from decimal import Decimal
# --- LISTAR FACTURAS ---
class FacturaListView(ListView):
    model = Factura
    template_name = 'factura/listar.html'
    context_object_name = 'facturas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Facturas'
        context['crear_url'] = reverse_lazy('app:crear_factura')
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        return context

# --- CREAR FACTURA ---
class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'factura/crear.html'
    success_url = reverse_lazy('app:listar_facturas')

    def form_valid(self, form):
        factura = form.save(commit=False)
        factura.subtotal = factura.venta.total
        factura.iva = factura.subtotal * Decimal('0.19')
        factura.total = factura.subtotal + factura.iva
        factura.save()
        messages.success(self.request, "Factura creada correctamente.")
        return super().form_valid(form)

# --- VER DETALLE (RECIBO) ---
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'factura/detalle.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Factura'
        return context

# --- ELIMINAR FACTURA ---
class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'factura/eliminar.html'
    success_url = reverse_lazy('app:listar_facturas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Factura'
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        return context