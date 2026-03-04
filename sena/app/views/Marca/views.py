from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from app.models import Marca
from app.forms import MarcaForm


# ================================
# LISTAR (Solo activas)
# ================================
class MarcaListView(ListView):
    model = Marca
    template_name = 'Marca/listar.html'
    context_object_name = 'marcas'

    def get_queryset(self):
        return Marca.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Marca'
        context['crear_url'] = reverse_lazy('app:crear_marca')
        context['listar_url'] = reverse_lazy('app:listar_marca')
        return context


# ================================
# CREAR
# ================================
class MarcaCreateView(SuccessMessageMixin, CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear.html'
    success_url = reverse_lazy('app:listar_marca')
    success_message = 'Marca creada exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Marca'
        context['listar_url'] = reverse_lazy('app:listar_marca')
        context['action'] = 'add'
        return context


# ================================
# EDITAR
# ================================
class MarcaUpdateView(SuccessMessageMixin, UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear.html'
    success_url = reverse_lazy('app:listar_marca')
    success_message = 'Marca actualizada exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Marca'
        context['listar_url'] = reverse_lazy('app:listar_marca')
        context['action'] = 'edit'
        return context


# ================================
# ELIMINAR O DESACTIVAR
# ================================
class MarcaDeleteView(View):

    def get(self, request, pk):
        marca = get_object_or_404(Marca, pk=pk)
        return render(request, 'Marca/eliminar.html', {
            'object': marca,
            'titulo': 'Eliminar Marca',
            'listar_url': reverse_lazy('app:listar_marca')
        })

    def post(self, request, pk):
        marca = get_object_or_404(Marca, pk=pk)

        accion = request.POST.get("accion")

        if accion == "desactivar":
            marca.estado = False
            marca.save()
            messages.success(request, "Marca desactivada correctamente.")
        else:
            marca.delete()
            messages.success(request, "Marca eliminada definitivamente.")

        return redirect('app:listar_marca')