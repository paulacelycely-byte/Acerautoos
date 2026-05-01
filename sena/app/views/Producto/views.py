from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin # Para permitir ver a todos

from app.models import Producto
from app.forms import ProductoForm
# --- IMPORTAMOS TU MIXIN DE ADMIN ---
from app.mixins import AdminRequeridoMixin 

STOCK_MINIMO_DEFAULT = 5

def get_stock_status(producto):
    """Devuelve 'sin', 'bajo' u 'ok' para un producto."""
    if producto.stock == 0:
        return 'sin'
    minimo = producto.stock_minimo if producto.stock_minimo > 0 else STOCK_MINIMO_DEFAULT
    if producto.stock <= minimo:
        return 'bajo'
    return 'ok'

# ─── LISTAR (MECÁNICO PUEDE ENTRAR) ──────────────────────
class ProductoListView(LoginRequiredMixin, ListView): 
    model = Producto
    template_name = 'producto/listar.html'
    context_object_name = 'productos'
    login_url = 'login:login'

    def get_queryset(self):
        qs = Producto.objects.select_related('marca', 'proveedor').order_by('-id')
        for p in qs:
            p.stock_status = get_stock_status(p)
            p.stock_minimo_efectivo = p.stock_minimo if p.stock_minimo > 0 else STOCK_MINIMO_DEFAULT
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Producto.objects.all()
        
        context['titulo'] = 'Inventario de Productos'
        context['crear_url'] = reverse_lazy('app:crear_producto')
        context['total_productos'] = qs.count()
        context['activos'] = qs.filter(estado=True).count()
        context['sin_stock'] = qs.filter(stock=0).count()
        context['stock_bajo'] = sum(1 for p in qs.filter(stock__gt=0) if get_stock_status(p) == 'bajo')
        context['valor_inventario'] = sum(p.precio * p.stock for p in qs.filter(estado=True))
        context['stock_minimo_default'] = STOCK_MINIMO_DEFAULT
        return context

# ─── CREAR (SOLO ADMIN) ──────────────────────────────────
class ProductoCreateView(AdminRequeridoMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    login_url = 'login:login'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url == 'orden':
            return reverse_lazy('app:orden_servicio_create')
        return reverse_lazy('app:listar_producto')

    def form_valid(self, form):
        messages.success(self.request, 'Producto creado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        context['next'] = self.request.GET.get('next', '')
        return context

# ─── EDITAR (SOLO ADMIN) ─────────────────────────────────
class ProductoUpdateView(AdminRequeridoMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('app:listar_producto')
    login_url = 'login:login'

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        context['next'] = self.request.GET.get('next', '')
        return context

# ─── ELIMINAR (SOLO ADMIN) ───────────────────────────────
class ProductoDeleteView(AdminRequeridoMixin, DeleteView):
    model = Producto
    template_name = 'producto/eliminar.html'
    success_url = reverse_lazy('app:listar_producto')
    login_url = 'login:login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Producto eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        return context