from django.views.generic import TemplateView
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app.models import Cliente, Vehiculo, Factura, Producto, Proveedor, Notificacion


def _verificar_mantenimientos():
    """Revisa todos los vehículos por km Y fecha — lo que llegue primero."""
    for vehiculo in Vehiculo.objects.select_related('marca', 'cliente').all():

        km_rest   = vehiculo.km_restantes_estimados()
        dias_rest = vehiculo.dias_restantes_mantenimiento()

        # Si no tiene ningún dato de mantenimiento configurado, saltar
        if km_rest is None and dias_rest is None:
            continue

        # ── Vencido ──
        vencido_km    = km_rest is not None and km_rest <= 0
        vencido_fecha = dias_rest is not None and dias_rest <= 0

        if vencido_km or vencido_fecha:
            razon  = "km vencidos" if vencido_km else "fecha vencida"
            titulo = f"Mantenimiento VENCIDO — {vehiculo.placa}"
            existe = Notificacion.objects.filter(titulo=titulo, leido=False).exists()
            if not existe:
                Notificacion.objects.create(
                    tipo     = 'Urgente',
                    origen   = 'SISTEMA',
                    titulo   = titulo,
                    vehiculo = vehiculo,
                    mensaje  = (
                        f"El vehículo {vehiculo.placa} ({vehiculo.marca.nombre} {vehiculo.modelo}) "
                        f"tiene el mantenimiento VENCIDO por {razon}. "
                        f"Km actuales estimados: {vehiculo.km_estimados_hoy():,}."
                    ),
                )
            continue

        # ── Próximo ──
        alerta_km    = km_rest is not None and km_rest <= vehiculo.km_alerta_anticipacion
        alerta_fecha = dias_rest is not None and dias_rest <= 15

        if alerta_km or alerta_fecha:
            razon  = f"~{km_rest:,} km restantes" if alerta_km else f"{dias_rest} días restantes"
            titulo = f"Mantenimiento próximo — {vehiculo.placa}"
            existe = Notificacion.objects.filter(titulo=titulo, leido=False).exists()
            if not existe:
                Notificacion.objects.create(
                    tipo     = 'Mantenimiento',
                    origen   = 'SISTEMA',
                    titulo   = titulo,
                    vehiculo = vehiculo,
                    mensaje  = (
                        f"El vehículo {vehiculo.placa} tiene su mantenimiento próximo. "
                        f"{razon}."
                    ),
                )


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """Dashboard principal — cambia según el rol del usuario"""
    
    def get_template_names(self):
        """Retorna el template según el cargo del usuario"""
        user = self.request.user
        
        # MECÁNICO — Dashboard simplificado
        if user.cargo == 'MECANICO':
            return ['dashboard/dashboard_mecanico.html']
        
        # ADMIN — Dashboard completo
        return ['dashboard/dashboard.html']

    def get_context_data(self, **kwargs):
        _verificar_mantenimientos()

        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # ── DATOS BÁSICOS PARA TODOS ──
        context['titulo']               = 'Panel de Control'
        context['total_notificaciones'] = Notificacion.objects.filter(leido=False).count()

        # ── SOLO PARA ADMIN ──
        if user.cargo == 'ADMIN':
            context['cant_vehiculos']       = Vehiculo.objects.count()
            context['cant_facturas']        = Factura.objects.count()
            context['cant_clientes']        = Cliente.objects.count()
            context['cant_productos']       = Producto.objects.count()
            context['cant_proveedores']     = Proveedor.objects.count()
            context['stock_bajo']           = Producto.objects.filter(stock__lte=F('stock_minimo')).count()
        
        # ── SOLO PARA MECÁNICO ──
        if user.cargo == 'MECANICO':
            context['cant_vehiculos']       = Vehiculo.objects.count()
            context['ordenes_pendientes']   = Notificacion.objects.filter(tipo='Mantenimiento', leido=False).count()

        return context