from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from app.models import Factura
from app.forms import FacturaForm
from django.contrib.auth.mixins import LoginRequiredMixin

# --- LISTAR FACTURAS ---
class FacturaListView(LoginRequiredMixin, ListView):
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
class FacturaCreateView(LoginRequiredMixin, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'factura/crear.html' 
    success_url = reverse_lazy('app:listar_facturas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Generar Nueva Factura'
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        return context

# --- VER DETALLE (RECIBO) ---
class FacturaDetailView(LoginRequiredMixin, DetailView):
    model = Factura
    template_name = 'factura/detalle.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Factura'
        return context

# --- ELIMINAR FACTURA ---
class FacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Factura
    template_name = 'factura/eliminar.html'
    success_url = reverse_lazy('app:listar_facturas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Factura'
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        return context