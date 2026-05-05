from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from app.models import Vehiculo, Notificacion
from app.forms import VehiculoForm

# ── MIXIN DE PROTECCIÓN PARA ADMINISTRADORES ─────────────────
class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        # Solo permite el acceso si el usuario es ADMIN o superusuario
        return self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos de administrador para realizar esta acción.")
        return redirect('app:listar_vehiculos')


# ── FUNCIONES DE CÁLCULO Y ALERTAS (Lógica original completa) ──
def _calcular_mantenimiento(vehiculo):
    """
    Calcula y asigna km_proximo_mantenimiento y fecha_proximo_mantenimiento
    a partir de km_ultimo_servicio, km_intervalo, fecha_ultimo_servicio e intervalo_meses.
    """
    # ── Próximo km ──
    if vehiculo.km_ultimo_servicio is not None and vehiculo.km_intervalo:
        vehiculo.km_proximo_mantenimiento = vehiculo.km_ultimo_servicio + vehiculo.km_intervalo
    else:
        vehiculo.km_proximo_mantenimiento = None

    # ── Próxima fecha ──
    # Si no tiene fecha de último servicio, usamos hoy como base
    base_fecha = vehiculo.fecha_ultimo_servicio or date.today()
    if vehiculo.intervalo_meses:
        vehiculo.fecha_proximo_mantenimiento = base_fecha + relativedelta(months=vehiculo.intervalo_meses)
    else:
        vehiculo.fecha_proximo_mantenimiento = None

    # ── Guardar fecha de último servicio si no tiene ──
    if not vehiculo.fecha_ultimo_servicio:
        vehiculo.fecha_ultimo_servicio = date.today()

    return vehiculo


def generar_alertas_km():
    """
    Revisa todos los vehículos y genera notificaciones automáticas
    para los que tienen km estimados dentro del rango de alerta.
    """
    for v in Vehiculo.objects.filter(km_proximo_mantenimiento__isnull=False):
        estado = v.estado_mantenimiento()
        if estado in ('alerta', 'vencido'):
            km_est       = v.km_estimados_hoy()
            km_restantes = v.km_restantes_estimados()
            titulo = (
                f"Mantenimiento vencido — {v.placa}"
                if estado == 'vencido'
                else f"Mantenimiento próximo — {v.placa}"
            )
            ya_existe = Notificacion.objects.filter(
                vehiculo=v,
                tipo='Mantenimiento',
                origen='SISTEMA',
                leido=False,
            ).exists()
            if not ya_existe:
                if estado == 'vencido':
                    msg = (
                        f"El vehículo {v.placa} ({v.marca.nombre} {v.modelo}) "
                        f"superó el límite de mantenimiento. "
                        f"Km actuales estimados: {km_est:,} km. "
                        f"Límite era: {v.km_proximo_mantenimiento:,} km."
                    )
                else:
                    msg = (
                        f"Faltan aprox. {max(int(km_restantes), 0):,} km para el próximo mantenimiento "
                        f"del vehículo {v.placa} ({v.marca.nombre} {v.modelo}). "
                        f"Próximo a los {v.km_proximo_mantenimiento:,} km."
                    )
                Notificacion.objects.create(
                    tipo    = 'Mantenimiento',
                    origen  = 'SISTEMA',
                    leido   = False,
                    vehiculo= v,
                    titulo  = titulo,
                    mensaje = msg,
                )


# ── 1. LISTADO (Acceso para Mecánicos y Admins) ──────────────
class VehiculoListView(LoginRequiredMixin, ListView):
    model = Vehiculo
    template_name = 'vehiculo/listar.html'
    context_object_name = 'vehiculos'

    def get_queryset(self):
        return Vehiculo.objects.select_related('marca', 'cliente').all()

    def get_context_data(self, **kwargs):
        generar_alertas_km()
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Vehículos'

        vehiculos_con_estado = []
        for v in context['vehiculos']:
            vehiculos_con_estado.append({
                'vehiculo'    : v,
                'km_estimados': v.km_estimados_hoy(),
                'km_restantes': v.km_restantes_estimados(),
                'dias_restantes': v.dias_restantes_mantenimiento(),
                'estado_mant' : v.estado_mantenimiento(),
            })
        context['vehiculos_con_estado'] = vehiculos_con_estado
        context['total_vencidos'] = sum(1 for x in vehiculos_con_estado if x['estado_mant'] == 'vencido')
        context['total_alertas']  = sum(1 for x in vehiculos_con_estado if x['estado_mant'] == 'alerta')
        return context


# ── 2. CREAR (Protegido - Solo Admin) ────────────────────────
class VehiculoCreateView(LoginRequiredMixin, SoloAdminMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Registrar Nuevo Vehículo'
        context['es_editar'] = False
        context['next']      = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        # Guardar sin commit para poder calcular los campos automáticos
        vehiculo = form.save(commit=False)
        vehiculo = _calcular_mantenimiento(vehiculo)
        vehiculo.save()
        form.save_m2m()

        self.object = vehiculo
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, f'Vehículo {vehiculo.placa} registrado con éxito en Acerautos.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)


# ── 3. EDITAR (Protegido - Solo Admin) ───────────────────────
class VehiculoUpdateView(LoginRequiredMixin, SoloAdminMixin, UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Editar Vehículo'
        context['es_editar'] = True
        context['next']      = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        # Guardar sin commit para recalcular los campos automáticos
        vehiculo = form.save(commit=False)
        vehiculo = _calcular_mantenimiento(vehiculo)
        vehiculo.save()
        form.save_m2m()

        self.object = vehiculo
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, f'Vehículo {vehiculo.placa} actualizado correctamente.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)


# ── 4. ELIMINAR (Protegido - Solo Admin) ─────────────────────
class VehiculoDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
    model = Vehiculo
    template_name = 'vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def form_valid(self, form):
        messages.success(self.request, 'El vehículo ha sido eliminado del sistema de Acerautos.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Vehículo'
        return context