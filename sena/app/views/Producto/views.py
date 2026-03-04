from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from app.models import Producto
from app.forms import ProductoForm


# ==============================
# LISTAR PRODUCTOS
# ==============================

class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/listar.html'
    context_object_name = 'producto'
    login_url = '/login/'

    def get_queryset(self):
        return Producto.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Producto'
        context['crear_url'] = reverse_lazy('app:crear_producto')
        return context


# ==============================
# CREAR PRODUCTO
# ==============================

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
        context['titulo'] = 'Crear Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        return context


# ==============================
# EDITAR PRODUCTO
# ==============================

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/editar.html'
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
        context['titulo'] = 'Editar Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        return context


# ==============================
# ELIMINAR PRODUCTO
# ==============================

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
        context['titulo'] = 'Eliminar Producto'
        context['listar_url'] = reverse_lazy('app:listar_producto')
        return context