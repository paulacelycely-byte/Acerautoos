from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from app.models import Producto
from app.forms import ProductoForm

STOCK_MINIMO_DEFAULT = 5

def get_stock_status(producto):
    """
    Devuelve 'sin', 'bajo' u 'ok' para un producto.
    Si stock_minimo == 0, usa STOCK_MINIMO_DEFAULT como fallback.
    """
    if producto.stock == 0:
        return 'sin'
    minimo = producto.stock_minimo if producto.stock_minimo > 0 else STOCK_MINIMO_DEFAULT
    if producto.stock <= minimo:
        return 'bajo'
    return 'ok'

class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/listar.html'
    context_object_name = 'productos'
    login_url = '/login/'

    def get_queryset(self):
        qs = Producto.objects.select_related('marca', 'proveedor').order_by('-id')
        # Anotar cada producto con su estado de stock calculado
        for p in qs:
            p.stock_status         = get_stock_status(p)
            p.stock_minimo_efectivo = p.stock_minimo if p.stock_minimo > 0 else STOCK_MINIMO_DEFAULT
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Producto.objects.all()

        total_productos  = qs.count()
        activos          = qs.filter(estado=True).count()
        sin_stock        = qs.filter(stock=0).count()
        stock_bajo       = sum(1 for p in qs.filter(stock__gt=0) if get_stock_status(p) == 'bajo')
        valor_inventario = sum(p.precio * p.stock for p in qs.filter(estado=True))

        context['titulo']               = 'Inventario de Productos'
        context['crear_url']            = reverse_lazy('app:crear_producto')
        context['total_productos']      = total_productos
        context['activos']              = activos
        context['sin_stock']            = sin_stock
        context['stock_bajo']           = stock_bajo
        context['valor_inventario']     = valor_inventario
        context['stock_minimo_default'] = STOCK_MINIMO_DEFAULT
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url == 'orden':
            return reverse_lazy('app:orden_servicio_create')
        return reverse_lazy('app:listar_producto')

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
        context['next']       = self.request.GET.get('next', '')
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('app:listar_producto')
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

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
        context['next']       = self.request.GET.get('next', '')
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