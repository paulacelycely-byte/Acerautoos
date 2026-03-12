from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View

from app.models import OrdenServicio, DetalleOrdenProducto
from app.forms import OrdenServicioForm


class OrdenServicioListView(ListView):
    model = OrdenServicio
    template_name = 'OrdenServicio/listar.html'
    context_object_name = 'ordenes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Órdenes de Servicio'
        return context


class OrdenServicioDetailView(View):
    def get(self, request, pk):
        orden = get_object_or_404(OrdenServicio, pk=pk)
        detalles = DetalleOrdenProducto.objects.filter(orden=orden).select_related('producto')

        # Calcular totales
        subtotal_productos = sum(
            d.producto.precio * d.cantidad for d in detalles
        )
        mano_obra = orden.servicio.precio_mano_obra
        total = subtotal_productos + mano_obra

        return render(request, 'OrdenServicio/detalle.html', {
            'orden'               : orden,
            'detalles'            : detalles,
            'subtotal_productos'  : subtotal_productos,
            'mano_obra'           : mano_obra,
            'total'               : total,
            'titulo'              : f'Detalle Orden #{orden.pk}',
            'listar_url'          : reverse_lazy('app:orden_servicio_list'),
        })


class OrdenServicioCreateView(CreateView):
    model = OrdenServicio
    form_class = OrdenServicioForm
    template_name = 'OrdenServicio/crear.html'
    success_url = reverse_lazy('app:orden_servicio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Orden de Servicio'
        context['listar_url'] = reverse_lazy('app:orden_servicio_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Orden de servicio creada correctamente.')
        return super().form_valid(form)


class OrdenServicioUpdateView(UpdateView):
    model = OrdenServicio
    form_class = OrdenServicioForm
    template_name = 'OrdenServicio/crear.html'
    success_url = reverse_lazy('app:orden_servicio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Orden de Servicio'
        context['listar_url'] = reverse_lazy('app:orden_servicio_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Orden de servicio actualizada correctamente.')
        return super().form_valid(form)


class OrdenServicioDeleteView(View):
    def get(self, request, pk):
        orden = get_object_or_404(OrdenServicio, pk=pk)
        return render(request, 'OrdenServicio/eliminar.html', {
            'object'    : orden,
            'titulo'    : 'Eliminar Orden de Servicio',
            'listar_url': reverse_lazy('app:orden_servicio_list')
        })

    def post(self, request, pk):
        orden = get_object_or_404(OrdenServicio, pk=pk)
        orden.delete()
        messages.success(request, 'Orden de servicio eliminada correctamente.')
        return redirect('app:orden_servicio_list')