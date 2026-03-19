from django.views.generic import TemplateView
from django.db.models import F

from app.models import Cliente, Vehiculo, Factura, Producto, Proveedor


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']           = 'Panel de Control'
        context['cant_vehiculos']   = Vehiculo.objects.count()
        context['cant_facturas']    = Factura.objects.count()
        context['cant_clientes']    = Cliente.objects.count()
        context['cant_productos']   = Producto.objects.count()
        context['cant_proveedores'] = Proveedor.objects.count()
        context['stock_bajo']       = Producto.objects.filter(
            stock__lte=F('stock_minimo')
        ).count()
        return context