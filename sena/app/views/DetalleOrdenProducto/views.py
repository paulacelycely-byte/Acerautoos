from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from app.models import OrdenServicio, DetalleOrdenProducto
from app.forms import DetalleOrdenProductoForm

class DetalleOrdenListView(ListView):
    model = DetalleOrdenProducto
    template_name = 'detalle/detalle_orden_list.html'
    context_object_name = 'detalles'

# Crear detalle
class DetalleOrdenCreateView(CreateView):
    model = DetalleOrdenProducto
    form_class = DetalleOrdenProductoForm
    template_name = 'detalle/detalle_orden_add.html'
    success_url = reverse_lazy('app:detalle_orden_list')

    def form_valid(self, form):
        try:
            form.instance.full_clean()
            form.save()
            messages.success(self.request, "Producto agregado correctamente")
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, str(e))
            return super().form_invalid(form)

# Editar detalle
class DetalleOrdenUpdateView(UpdateView):
    model = DetalleOrdenProducto
    form_class = DetalleOrdenProductoForm
    template_name = 'detalle/detalle_orden_add.html'
    success_url = reverse_lazy('app:detalle_orden_list')

# Eliminar detalle
class DetalleOrdenDeleteView(DeleteView):
    model = DetalleOrdenProducto
    template_name = 'detalle/detalle_orden_confirm_delete.html'
    success_url = reverse_lazy('app:detalle_orden_list')