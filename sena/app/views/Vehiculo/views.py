from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from app.models import Vehiculo, Notificacion
from app.forms import VehiculoForm


def generar_alertas_km():
    """
    Revisa todos los vehículos y genera notificaciones automáticas
    para los que tienen km estimados dentro del rango de alerta.
    Se llama cada vez que se carga el listado.
    """
    for v in Vehiculo.objects.filter(km_proximo_mantenimiento__isnull=False):
        estado = v.estado_mantenimiento()
        if estado in ('alerta', 'vencido'):
            km_est      = v.km_estimados_hoy()
            km_restantes = v.km_restantes_estimados()
            titulo = f"{'⚠ Mantenimiento vencido' if estado == 'vencido' else '🔔 Mantenimiento próximo'} — {v.placa}"
            # Solo crear si no existe una notificación no leída reciente para este vehículo
            ya_existe = Notificacion.objects.filter(
                vehiculo = v,
                tipo     = 'Mantenimiento',
                origen   = 'SISTEMA',
                leido    = False,
            ).exists()
            if not ya_existe:
                Notificacion.objects.create(
                    tipo     = 'Mantenimiento',
                    origen   = 'SISTEMA',
                    leido    = False,
                    vehiculo = v,
                    titulo   = titulo,
                    mensaje  = (
                        f"El vehículo {v.placa} ({v.marca.nombre} {v.modelo}) "
                        f"tiene estimados {km_est:,} km actuales. "
                        f"Próximo mantenimiento a los {v.km_proximo_mantenimiento:,} km. "
                        f"{'¡Ya superó el límite!' if estado == 'vencido' else f'Faltan aprox. {max(km_restantes, 0):,} km.'}"
                    ),
                )


# 1. LISTADO
class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'vehiculo/listar.html'
    context_object_name = 'vehiculos'

    def get_queryset(self):
        return Vehiculo.objects.select_related('marca', 'cliente').all()

    def get_context_data(self, **kwargs):
        # Generar alertas automáticas al cargar el listado
        generar_alertas_km()

        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Vehículos'

        # Agregar datos de mantenimiento a cada vehículo para el template
        hoy = timezone.now().date()
        vehiculos_con_estado = []
        for v in context['vehiculos']:
            vehiculos_con_estado.append({
                'vehiculo'       : v,
                'km_estimados'   : v.km_estimados_hoy(),
                'km_restantes'   : v.km_restantes_estimados(),
                'estado_mant'    : v.estado_mantenimiento(),
            })
        context['vehiculos_con_estado'] = vehiculos_con_estado

        # Contadores para el header
        context['total_vencidos'] = sum(1 for x in vehiculos_con_estado if x['estado_mant'] == 'vencido')
        context['total_alertas']  = sum(1 for x in vehiculos_con_estado if x['estado_mant'] == 'alerta')

        return context


# 2. CREAR
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
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Vehículo registrado con éxito en Acerautos.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)


# 3. EDITAR
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
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Datos del vehículo actualizados correctamente.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)


# 4. ELIMINAR
class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    template_name = 'vehiculo/eliminar.html'
    success_url = reverse_lazy('app:listar_vehiculos')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'El vehículo ha sido eliminado del sistema.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Vehículo'
        return context