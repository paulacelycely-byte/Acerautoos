from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from ...models import CompatibilidadProducto
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
    form_class = CompatibilidadProductoForm  # ← USA EL FORM CORRECTO
    template_name = 'compatibilidadProducto/crear.html'
    success_url = reverse_lazy('app:listar_compatibilidad')
    success_message = 'Compatibilidad registrada exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Compatibilidad'
        return context


class CompatibilidadUpdateView(SuccessMessageMixin, UpdateView):
    model = CompatibilidadProducto
    form_class = CompatibilidadProductoForm  # ← USA EL FORM CORRECTO
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