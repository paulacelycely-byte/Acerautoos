from django.views.generic import TemplateView
from app.models import Vehiculo, Ventas, Cliente, Producto, Proveedor # Importa tus modelos reales

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Panel de Control'
        
        # Estas variables alimentarán las tarjetas de arriba
        context['cant_vehiculos'] = Vehiculo.objects.count()
        context['cant_ventas'] = Ventas.objects.count()
        context['cant_clientes'] = Cliente.objects.count()
        context['cant_productos'] = Producto.objects.count()
        context['cant_proveedores'] = Proveedor.objects.count()
        
        return context