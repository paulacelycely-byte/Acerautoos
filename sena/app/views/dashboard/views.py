from django.views.generic import TemplateView
from django.db.models import F
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from app.models import Cliente, Vehiculo, Factura, Producto, Proveedor, Notificacion


def _verificar_mantenimientos():
    """Revisa todos los vehículos y crea notificaciones si es necesario."""
    for vehiculo in Vehiculo.objects.select_related('marca', 'cliente').all():
        if not vehiculo.km_proximo_mantenimiento:
            continue

        restantes = vehiculo.km_restantes_estimados()
        if restantes is None:
            continue

        if restantes <= 0:
            titulo = f"Mantenimiento VENCIDO — {vehiculo.placa}"
        elif restantes <= vehiculo.km_alerta_anticipacion:
            titulo = f"Mantenimiento próximo — {vehiculo.placa}"
        else:
            continue

        # Solo crear si no existe una notificación no leída igual
        existe = Notificacion.objects.filter(titulo=titulo, leido=False).exists()
        if not existe:
            tipo   = 'Urgente' if restantes <= 0 else 'Mantenimiento'
            km_txt = f"vencido por {abs(restantes):,} km" if restantes <= 0 else f"~{restantes:,} km restantes"
            Notificacion.objects.create(
                tipo     = tipo,
                origen   = 'SISTEMA',
                titulo   = titulo,
                vehiculo = vehiculo,
                mensaje  = (
                    f"El vehículo {vehiculo.placa} ({vehiculo.marca.nombre} {vehiculo.modelo}) "
                    f"tiene su mantenimiento {km_txt}. "
                    f"Km programado: {vehiculo.km_proximo_mantenimiento:,}."
                ),
            )


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        # Verificar mantenimientos cada vez que se carga el dashboard
        _verificar_mantenimientos()

        context = super().get_context_data(**kwargs)
        context['titulo']              = 'Panel de Control'
        context['cant_vehiculos']      = Vehiculo.objects.count()
        context['cant_facturas']       = Factura.objects.count()
        context['cant_clientes']       = Cliente.objects.count()
        context['cant_productos']      = Producto.objects.count()
        context['cant_proveedores']    = Proveedor.objects.count()
        context['stock_bajo']          = Producto.objects.filter(stock__lte=F('stock_minimo')).count()
        context['total_notificaciones'] = Notificacion.objects.filter(leido=False).count()
        return context