from django.views.generic import TemplateView
from django.db.models import F
from app.models import Vehiculo, VentasFactura, Cliente, Producto, Proveedor 

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Panel de Control'
        
        context['cant_vehiculos']  = Vehiculo.objects.count()
        context['cant_ventas']     = VentasFactura.objects.count() 
        context['cant_clientes']   = Cliente.objects.count()
        context['cant_productos']  = Producto.objects.count()
        context['cant_proveedores']= Proveedor.objects.count()
        
        # ✅ Corregido: 'existencia' → 'stock'
        context['stock_bajo'] = Producto.objects.filter(
            stock__lte=F('stock_minimo')
        ).count()
        
        return context