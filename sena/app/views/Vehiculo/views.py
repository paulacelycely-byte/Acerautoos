from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta

from app.models import Vehiculo, Notificacion
from app.forms import VehiculoForm


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


# ── 1. LISTADO ──────────────────────────────────────────────
class VehiculoListView(ListView):
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


# ── 2. CREAR ────────────────────────────────────────────────
class VehiculoCreateView(CreateView):
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
        messages.success(self.request, f'Vehículo {vehiculo.placa} registrado con éxito.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)


# ── 3. EDITAR ───────────────────────────────────────────────
class VehiculoUpdateView(UpdateView):
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


# ── 4. ELIMINAR ─────────────────────────────────────────────
class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    template_name = 'vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def form_valid(self, form):
        messages.success(self.request, 'El vehículo ha sido eliminado del sistema.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Vehículo'
        return context