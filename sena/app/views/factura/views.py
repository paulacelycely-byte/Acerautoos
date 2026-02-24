from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from app.models import Factura
from app.forms import FacturaForm

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

class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'factura/crear.html' # Reutiliza el estilo de crear.html de compras
    success_url = reverse_lazy('app:listar_facturas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        return context

class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'factura/detalle.html'
    context_object_name = 'factura'

class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'factura/eliminar.html'
    success_url = reverse_lazy('app:listar_facturas')