from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from app.models import Producto
from app.forms import ProductoForm


class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/listar.html'
    context_object_name = 'productos'
    login_url = '/login/'

    def get_queryset(self):
        return Producto.objects.select_related('marca', 'proveedor').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Producto.objects.all()

        total_productos  = qs.count()
        activos          = qs.filter(estado=True).count()
        sin_stock        = qs.filter(stock=0).count()
        # Stock bajo: tiene stock pero está en o por debajo del mínimo
        stock_bajo       = sum(1 for p in qs.filter(stock__gt=0) if p.stock <= p.stock_minimo)
        valor_inventario = sum(p.precio * p.stock for p in qs.filter(estado=True))

        context['titulo']           = 'Inventario de Productos'
        context['crear_url']        = reverse_lazy('app:crear_producto')
        context['total_productos']  = total_productos
        context['activos']          = activos
        context['sin_stock']        = sin_stock
        context['stock_bajo']       = stock_bajo
        context['valor_inventario'] = valor_inventario
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('app:listar_producto')
    login_url = '/login/'

    def form_valid(self, form):
        messages.success(self.request, 'Producto creado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el producto. Verifique los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Crear Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('app:listar_producto')
    login_url = '/login/'

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el producto.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Editar Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto/eliminar.html'
    success_url = reverse_lazy('app:listar_producto')
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Producto eliminado correctamente.')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Eliminar Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        return context