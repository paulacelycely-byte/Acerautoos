from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from app.models import Compra
from app.forms import CompraForm

# --- VISTA PARA LISTAR COMPRAS ---
class CompraListView(ListView):
    model = Compra
    template_name = 'compra/listar.html'
    context_object_name = 'compras'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Compras'
        context['crear_url'] = reverse_lazy('app:crear_compra')
        context['listar_url'] = reverse_lazy('app:listar_compras')
        return context

# --- VISTA PARA CREAR COMPRA ---
class CompraCreateView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compra/crear.html'
    success_url = reverse_lazy('app:listar_compras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listar_url'] = reverse_lazy('app:listar_compras')
        context['titulo'] = 'Nueva Compra'
        return context

# --- VISTA PARA EDITAR COMPRA ---
class CompraUpdateView(UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compra/crear.html'
    success_url = reverse_lazy('app:listar_compras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listar_url'] = reverse_lazy('app:listar_compras')
        context['titulo'] = 'Editar Compra'
        return context

# --- VISTA PARA ELIMINAR COMPRA ---
class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'compra/eliminar.html'
    success_url = reverse_lazy('app:listar_compras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listar_url'] = reverse_lazy('app:listar_compras')
        context['titulo'] = 'Eliminar Compra'
        return context