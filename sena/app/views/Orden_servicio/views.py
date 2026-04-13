from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse

from app.models import OrdenServicio, DetalleOrdenProducto, Vehiculo, Producto, CompatibilidadProducto
from app.forms import OrdenServicioForm


# ══════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════

def _verificar_compat(producto, marca_id, servicio_id=None):
    total = CompatibilidadProducto.objects.filter(producto=producto).count()
    if total == 0:
        return 'neutral', ''
    qs = CompatibilidadProducto.objects.filter(producto=producto, marca_vehiculo_id=marca_id)
    if servicio_id and qs.filter(tipo_servicio_id=servicio_id).exists():
        return 'ok', f'{producto.nombre} es compatible con esta marca y servicio.'
    if qs.filter(tipo_servicio__isnull=True).exists():
        return 'ok', f'{producto.nombre} es compatible con esta marca.'
    marcas_ok = list(
        CompatibilidadProducto.objects
        .filter(producto=producto)
        .values_list('marca_vehiculo__nombre', flat=True)
        .distinct()
    )
    return 'warn', f'{producto.nombre} no aplica para esta marca. Aplica para: {", ".join(marcas_ok)}.'


def _get_productos_disponibles():
    return Producto.objects.filter(estado=True, stock__gt=0).order_by('nombre')


def _guardar_productos(request, orden):
    producto_ids = request.POST.getlist('producto_ids[]')
    cantidades   = request.POST.getlist('producto_cantidades[]')
    for pid, cant in zip(producto_ids, cantidades):
        try:
            prod = Producto.objects.get(pk=pid, estado=True)
            DetalleOrdenProducto.objects.create(
                orden=orden, producto=prod, cantidad=max(1, int(cant))
            )
        except (Producto.DoesNotExist, ValueError):
            continue


def _hay_incompatibles(request, marca_id, servicio_ids):
    """
    Solo bloquea si el producto tiene reglas de compatibilidad definidas
    Y no es compatible con ninguno de los servicios de la orden.
    Si no tiene reglas (neutral) o es compatible con al menos uno, lo deja pasar.
    """
    for pid in request.POST.getlist('producto_ids[]'):
        try:
            prod = Producto.objects.get(pk=pid, estado=True)

            # Sin reglas configuradas = neutral, no bloquear
            total_reglas = CompatibilidadProducto.objects.filter(producto=prod).count()
            if total_reglas == 0:
                continue

            # Verificar si es compatible con AL MENOS un servicio de la orden
            es_compatible = False
            for sid in servicio_ids:
                status, _ = _verificar_compat(prod, marca_id, sid)
                if status in ('ok', 'neutral'):
                    es_compatible = True
                    break

            # Si no encontró compatibilidad con ningún servicio, bloquear
            if not es_compatible:
                return True

        except Producto.DoesNotExist:
            continue
    return False


# ══════════════════════════════════════════════════════════
#  LISTAR
# ══════════════════════════════════════════════════════════

class OrdenServicioListView(ListView):
    model = OrdenServicio
    template_name = 'OrdenServicio/listar.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related(
            'servicios',
            'productos_usados__producto__compatibilidadproducto_set'
        )
        for orden in qs:
            marca_id     = orden.vehiculo.marca_id
            servicio_ids = list(orden.servicios.values_list('id', flat=True))
            tiene_warn   = False
            for detalle in orden.productos_usados.all():
                for sid in servicio_ids:
                    status, _ = _verificar_compat(detalle.producto, marca_id, sid)
                    if status == 'warn':
                        tiene_warn = True
                        break
                if tiene_warn:
                    break
            orden.tiene_incompatibles = tiene_warn
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Órdenes de Servicio'
        return context


# ══════════════════════════════════════════════════════════
#  DETALLE
# ══════════════════════════════════════════════════════════

class OrdenServicioDetailView(View):
    def get(self, request, pk):
        orden    = get_object_or_404(OrdenServicio, pk=pk)
        detalles = DetalleOrdenProducto.objects.filter(orden=orden).select_related('producto')
        marca_id     = orden.vehiculo.marca_id
        servicio_ids = list(orden.servicios.values_list('id', flat=True))

        for d in detalles:
            sid = servicio_ids[0] if servicio_ids else None
            d.compat_status, d.compat_mensaje = _verificar_compat(d.producto, marca_id, sid)

        mano_obra          = sum(s.precio_mano_obra for s in orden.servicios.all())
        subtotal_productos = sum(d.producto.precio * d.cantidad for d in detalles)
        total              = subtotal_productos + mano_obra

        return render(request, 'OrdenServicio/detalle.html', {
            'orden':               orden,
            'detalles':            detalles,
            'subtotal_productos':  subtotal_productos,
            'mano_obra':           mano_obra,
            'total':               total,
            'titulo':              f'Detalle Orden #{orden.pk}',
            'listar_url':          reverse_lazy('app:orden_servicio_list'),
        })


# ══════════════════════════════════════════════════════════
#  AJAX — KM VEHÍCULO
# ══════════════════════════════════════════════════════════

class VehiculoKmView(View):
    def get(self, request, pk):
        try:
            v = Vehiculo.objects.select_related('marca').get(pk=pk)
            return JsonResponse({
                'km':           v.km_ultimo_servicio or 0,
                'placa':        v.placa,
                'marca_id':     v.marca_id,
                'marca_nombre': v.marca.nombre,
            })
        except Vehiculo.DoesNotExist:
            return JsonResponse({'km': 0}, status=404)


# ══════════════════════════════════════════════════════════
#  AJAX — VERIFICAR COMPATIBILIDAD
# ══════════════════════════════════════════════════════════

class VerificarCompatibilidadView(View):
    def get(self, request):
        producto_id = request.GET.get('producto')
        marca_id    = request.GET.get('marca')
        servicio_id = request.GET.get('servicio')
        if not producto_id or not marca_id:
            return JsonResponse({'compatible': None, 'tiene_reglas': False, 'mensaje': ''})
        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            return JsonResponse({'compatible': None, 'tiene_reglas': False, 'mensaje': ''})
        status, mensaje = _verificar_compat(producto, marca_id, servicio_id)
        if status == 'neutral':
            return JsonResponse({'compatible': None,  'tiene_reglas': False, 'mensaje': ''})
        elif status == 'ok':
            return JsonResponse({'compatible': True,  'tiene_reglas': True,  'mensaje': mensaje})
        else:
            return JsonResponse({'compatible': False, 'tiene_reglas': True,  'mensaje': mensaje})


# ══════════════════════════════════════════════════════════
#  AJAX — PRODUCTOS COMPATIBLES
# ══════════════════════════════════════════════════════════

class ProductosCompatiblesView(View):
    def get(self, request):
        marca_id    = request.GET.get('marca')
        servicio_id = request.GET.get('servicio')
        if not marca_id:
            return JsonResponse({'productos': []})
        qs_base = CompatibilidadProducto.objects.filter(
            marca_vehiculo_id=marca_id
        ).select_related('producto')
        qs = (
            qs_base.filter(tipo_servicio_id=servicio_id) |
            qs_base.filter(tipo_servicio__isnull=True)
        ) if servicio_id else qs_base
        productos, vistos = [], set()
        for comp in qs:
            if comp.producto_id not in vistos and comp.producto.estado:
                vistos.add(comp.producto_id)
                productos.append({
                    'id':     comp.producto.pk,
                    'nombre': comp.producto.nombre,
                    'stock':  comp.producto.stock,
                    'precio': float(comp.producto.precio),
                })
        return JsonResponse({'productos': productos})


# ══════════════════════════════════════════════════════════
#  CREAR ORDEN
# ══════════════════════════════════════════════════════════

class OrdenServicioCreateView(CreateView):
    model         = OrdenServicio
    form_class    = OrdenServicioForm
    template_name = 'OrdenServicio/crear.html'
    success_url   = reverse_lazy('app:orden_servicio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']                = 'Nueva Orden de Servicio'
        context['listar_url']            = reverse_lazy('app:orden_servicio_list')
        context['es_editar']             = False
        context['productos_disponibles'] = _get_productos_disponibles()
        return context

    def form_valid(self, form):
        orden = form.save(commit=False)

        if orden.vehiculo and orden.km_actual and orden.km_actual > (orden.vehiculo.km_ultimo_servicio or 0):
            orden.vehiculo.km_ultimo_servicio = orden.km_actual
            orden.vehiculo.save(update_fields=['km_ultimo_servicio'])

        orden.save()
        form.save_m2m()

        servicio_ids = list(orden.servicios.values_list('id', flat=True))

        if _hay_incompatibles(self.request, orden.vehiculo.marca_id, servicio_ids):
            messages.error(
                self.request,
                '⚠ No se puede guardar: hay productos incompatibles con la marca de este vehículo. '
                'Retira o reemplaza los productos marcados en amarillo.'
            )
            orden.delete()
            return self.form_invalid(form)

        _guardar_productos(self.request, orden)

        messages.success(self.request, 'Orden de servicio creada correctamente.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        print("ERRORES FORM ORDEN:", form.errors)
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


# ══════════════════════════════════════════════════════════
#  EDITAR ORDEN
# ══════════════════════════════════════════════════════════

class OrdenServicioUpdateView(UpdateView):
    model         = OrdenServicio
    form_class    = OrdenServicioForm
    template_name = 'OrdenServicio/crear.html'
    success_url   = reverse_lazy('app:orden_servicio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']                = 'Editar Orden de Servicio'
        context['listar_url']            = reverse_lazy('app:orden_servicio_list')
        context['es_editar']             = True
        context['productos_disponibles'] = _get_productos_disponibles()
        return context

    def form_valid(self, form):
        orden = form.save(commit=False)

        if orden.vehiculo and orden.km_actual and orden.km_actual > (orden.vehiculo.km_ultimo_servicio or 0):
            orden.vehiculo.km_ultimo_servicio = orden.km_actual
            orden.vehiculo.save(update_fields=['km_ultimo_servicio'])

        orden.save()
        form.save_m2m()

        servicio_ids = list(orden.servicios.values_list('id', flat=True))

        if _hay_incompatibles(self.request, orden.vehiculo.marca_id, servicio_ids):
            messages.error(
                self.request,
                '⚠ No se puede guardar: hay productos incompatibles con la marca de este vehículo. '
                'Retira o reemplaza los productos marcados en amarillo.'
            )
            return self.form_invalid(form)

        orden.productos_usados.all().delete()
        _guardar_productos(self.request, orden)

        messages.success(self.request, 'Orden de servicio actualizada correctamente.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        print("ERRORES FORM ORDEN:", form.errors)
        return super().form_invalid(form)


# ══════════════════════════════════════════════════════════
#  ELIMINAR ORDEN
# ══════════════════════════════════════════════════════════

class OrdenServicioDeleteView(View):
    def get(self, request, pk):
        orden = get_object_or_404(OrdenServicio, pk=pk)
        return render(request, 'OrdenServicio/eliminar.html', {
            'object':     orden,
            'titulo':     'Eliminar Orden de Servicio',
            'listar_url': reverse_lazy('app:orden_servicio_list'),
        })

    def post(self, request, pk):
        orden = get_object_or_404(OrdenServicio, pk=pk)
        orden.delete()
        messages.success(request, 'Orden de servicio eliminada correctamente.')
        return redirect('app:orden_servicio_list')