from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.http import JsonResponse

from ...models import CompatibilidadProducto, Producto, Marca
from ...forms import CompatibilidadProductoForm


class CompatibilidadListView(ListView):
    model = CompatibilidadProducto
    template_name = 'compatibilidadProducto/listar.html'
    context_object_name = 'compatibilidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Compatibilidad de Productos'
        return context


class CompatibilidadCreateView(SuccessMessageMixin, CreateView):
    model = CompatibilidadProducto
    form_class = CompatibilidadProductoForm
    template_name = 'compatibilidadProducto/crear.html'
    success_url = reverse_lazy('app:listar_compatibilidad')
    success_message = 'Compatibilidad registrada exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Compatibilidad'
        return context


class CompatibilidadUpdateView(SuccessMessageMixin, UpdateView):
    model = CompatibilidadProducto
    form_class = CompatibilidadProductoForm
    template_name = 'compatibilidadProducto/crear.html'
    success_url = reverse_lazy('app:listar_compatibilidad')
    success_message = 'Compatibilidad actualizada exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Compatibilidad'
        return context


class CompatibilidadDeleteView(View):
    def get(self, request, pk):
        comp = get_object_or_404(CompatibilidadProducto, pk=pk)
        return render(request, 'compatibilidadProducto/eliminar.html', {
            'object': comp,
            'titulo': 'Eliminar Compatibilidad',
            'listar_url': reverse_lazy('app:listar_compatibilidad')
        })

    def post(self, request, pk):
        comp = get_object_or_404(CompatibilidadProducto, pk=pk)
        comp.delete()
        messages.success(request, 'Compatibilidad eliminada correctamente.')
        return redirect('app:listar_compatibilidad')


# ─── Endpoint AJAX: verifica compatibilidad de un producto con la marca del vehículo ───
class VerificarCompatibilidadView(View):
    """
    GET /orden_servicio/verificar-compatibilidad/?producto=X&marca=Y&servicio=Z
    Devuelve:
      {
        "compatible": true/false/null,   # null = sin reglas definidas
        "mensaje": "...",
        "tiene_reglas": true/false       # si el producto tiene alguna compatibilidad configurada
      }
    """
    def get(self, request):
        producto_id = request.GET.get('producto')
        marca_id    = request.GET.get('marca')       # marca del vehículo de la orden
        servicio_id = request.GET.get('servicio')    # tipo de servicio de la orden

        if not producto_id or not marca_id:
            return JsonResponse({'compatible': None, 'tiene_reglas': False, 'mensaje': ''})

        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            return JsonResponse({'compatible': None, 'tiene_reglas': False, 'mensaje': ''})

        # ¿El producto tiene alguna regla de compatibilidad definida?
        total_reglas = CompatibilidadProducto.objects.filter(producto=producto).count()

        if total_reglas == 0:
            # Sin reglas → no hay restricción, no mostrar nada
            return JsonResponse({
                'compatible': None,
                'tiene_reglas': False,
                'mensaje': ''
            })

        # Buscar compatibilidad exacta: marca + servicio
        qs = CompatibilidadProducto.objects.filter(producto=producto, marca_vehiculo_id=marca_id)

        # Primero intenta match exacto con servicio
        if servicio_id:
            match_exacto = qs.filter(servicio_id=servicio_id).exists()
            if match_exacto:
                return JsonResponse({
                    'compatible': True,
                    'tiene_reglas': True,
                    'mensaje': f'✓ {producto.nombre} es compatible con esta marca y este servicio.'
                })

        # Luego intenta match solo con marca (sin restricción de servicio)
        match_marca = qs.filter(tipo_servicio__isnull=True).exists()
        if match_marca:
            return JsonResponse({
                'compatible': True,
                'tiene_reglas': True,
                'mensaje': f'✓ {producto.nombre} es compatible con esta marca de vehículo.'
            })

        # Tiene reglas pero no aplica para esta marca
        # Obtener para qué marcas sí aplica
        marcas_ok = list(
            CompatibilidadProducto.objects
            .filter(producto=producto)
            .values_list('marca_vehiculo__nombre', flat=True)
            .distinct()
        )
        marcas_str = ', '.join(marcas_ok) if marcas_ok else 'otras marcas'

        return JsonResponse({
            'compatible': False,
            'tiene_reglas': True,
            'mensaje': f'⚠ {producto.nombre} no tiene compatibilidad registrada para esta marca. Aplica para: {marcas_str}.'
        })


# ─── Endpoint AJAX: devuelve productos compatibles con una marca/servicio ───
class ProductosCompatiblesView(View):
    """
    GET /orden_servicio/productos-compatibles/?marca=Y&servicio=Z
    Devuelve lista de productos compatibles con esa marca/servicio para resaltarlos en el selector.
    """
    def get(self, request):
        marca_id    = request.GET.get('marca')
        servicio_id = request.GET.get('servicio')

        if not marca_id:
            return JsonResponse({'productos': []})

        qs = CompatibilidadProducto.objects.filter(
            marca_vehiculo_id=marca_id
        ).select_related('producto')

        if servicio_id:
            qs = qs.filter(
                tipo_servicio_id=servicio_id
            ) | CompatibilidadProducto.objects.filter(
                marca_vehiculo_id=marca_id,
                tipo_servicio__isnull=True
            ).select_related('producto')

        productos = []
        vistos = set()
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