from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from app.models import Vehiculo, Notificacion
from app.forms import VehiculoForm

# ── MIXIN DE PROTECCIÓN PARA ADMINISTRADORES ─────────────────
class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos de administrador para realizar esta acción.")
        return redirect('app:listar_vehiculos')


# ── FUNCIONES DE CÁLCULO Y ALERTAS ──
def _calcular_mantenimiento(vehiculo):
    """
    Calcula la lógica de mantenimiento. 
    Se eliminó 'fecha_ultimo_servicio' porque no existe en el modelo.
    """
    # Usamos la fecha de hoy como base para cualquier cálculo interno
    # La fecha_proximo_mantenimiento ya viene del formulario
    return vehiculo


def generar_alertas_mantenimiento():
    """
    Genera notificaciones basadas únicamente en la fecha de mantenimiento.
    """
    hoy = date.today()
    for v in Vehiculo.objects.filter(fecha_proximo_mantenimiento__isnull=False):
        dias_para = (v.fecha_proximo_mantenimiento - hoy).days
        
        estado = 'ok'
        if dias_para <= 0:
            estado = 'vencido'
        elif dias_para <= 15:
            estado = 'alerta'

        if estado in ('alerta', 'vencido'):
            titulo = (
                f"Mantenimiento VENCIDO — {v.placa}"
                if estado == 'vencido'
                else f"Mantenimiento PRÓXIMO — {v.placa}"
            )
            
            ya_existe = Notificacion.objects.filter(
                vehiculo=v,
                tipo='Mantenimiento',
                origen='SISTEMA',
                leido=False,
                titulo=titulo
            ).exists()

            if not ya_existe:
                if estado == 'vencido':
                    msg = f"El vehículo {v.placa} superó la fecha límite ({v.fecha_proximo_mantenimiento})."
                else:
                    msg = f"El vehículo {v.placa} tiene su próximo servicio el {v.fecha_proximo_mantenimiento} ({dias_para} días restantes)."

                Notificacion.objects.create(
                    tipo='Mantenimiento',
                    origen='SISTEMA',
                    leido=False,
                    vehiculo=v,
                    titulo=titulo,
                    mensaje=msg,
                )


# ── 1. LISTADO ──────────────────────────────────────────────
class VehiculoListView(LoginRequiredMixin, ListView):
    model = Vehiculo
    template_name = 'vehiculo/listar.html'
    context_object_name = 'vehiculos'

    def get_queryset(self):
        return Vehiculo.objects.select_related('marca', 'cliente').all()

    def get_context_data(self, **kwargs):
        generar_alertas_mantenimiento()
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Vehículos'

        vehiculos_con_estado = []
        hoy = date.today()

        for v in context['vehiculos']:
            dias = None
            estado = 'sin_datos'
            
            if v.fecha_proximo_mantenimiento:
                dias = (v.fecha_proximo_mantenimiento - hoy).days
                if dias <= 0:
                    estado = 'vencido'
                elif dias <= 15:
                    estado = 'alerta'
                else:
                    estado = 'ok'

            vehiculos_con_estado.append({
                'vehiculo': v,
                'km_restantes': None,
                'dias_restantes': dias,
                'estado_mant': estado,
            })

        context['vehiculos_con_estado'] = vehiculos_con_estado
        context['total_vencidos'] = sum(1 for x in vehiculos_con_estado if x['estado_mant'] == 'vencido')
        context['total_alertas'] = sum(1 for x in vehiculos_con_estado if x['estado_mant'] == 'alerta')
        return context


# ── 2. CREAR ─────────────────────────────────────────────────
class VehiculoCreateView(LoginRequiredMixin, SoloAdminMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nuevo Vehículo'
        context['es_editar'] = False
        context['next'] = self.request.GET.get('next', '')
        
        # Esto reemplaza el filtro 'split_usage' que te daba error en el HTML
        context['opciones_uso'] = [
            {'val': 'BAJO', 'label': 'Uso Bajo', 'img': 'ciudadvehiculo.jpeg', 'desc': '~30 km/día'},
            {'val': 'NORMAL', 'label': 'Uso Normal', 'img': 'vehiculoo.jpeg', 'desc': '~50 km/día'},
            {'val': 'ALTO', 'label': 'Uso Alto', 'img': 'viajevehiculo.jpeg', 'desc': '~80 km/día'},
            {'val': 'CARGA', 'label': 'Carga', 'img': 'carga.jpeg', 'desc': '~120 km/día'},
        ]
        return context

    def form_valid(self, form):
        vehiculo = form.save(commit=False)
        vehiculo = _calcular_mantenimiento(vehiculo)
        vehiculo.save()
        form.save_m2m()

        messages.success(self.request, f'Vehículo {vehiculo.placa} registrado con éxito.')
        next_param = self.request.POST.get('next', '')
        if next_param == 'orden':
            return redirect('app:orden_servicio_create')
        return redirect(self.success_url)


# ── 3. EDITAR ────────────────────────────────────────────────
class VehiculoUpdateView(LoginRequiredMixin, SoloAdminMixin, UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/crear.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Vehículo'
        context['es_editar'] = True
        context['next'] = self.request.GET.get('next', '')
        
        # También lo agregamos aquí para que al editar no falle el grid
        context['opciones_uso'] = [
            {'val': 'BAJO', 'label': 'Uso Bajo', 'img': 'ciudadvehiculo.jpeg', 'desc': '~30 km/día'},
            {'val': 'NORMAL', 'label': 'Uso Normal', 'img': 'vehiculoo.jpeg', 'desc': '~50 km/día'},
            {'val': 'ALTO', 'label': 'Uso Alto', 'img': 'viajevehiculo.jpeg', 'desc': '~80 km/día'},
            {'val': 'CARGA', 'label': 'Carga', 'img': 'carga.jpeg', 'desc': '~120 km/día'},
        ]
        return context

    def form_valid(self, form):
        vehiculo = form.save(commit=False)
        vehiculo = _calcular_mantenimiento(vehiculo)
        vehiculo.save()
        form.save_m2m()

        messages.success(self.request, f'Vehículo {vehiculo.placa} actualizado correctamente.')
        next_param = self.request.POST.get('next', '')
        if next_param == 'orden':
            return redirect('app:orden_servicio_create')
        return redirect(self.success_url)


# ── 4. ELIMINAR ──────────────────────────────────────────────
class VehiculoDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
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