from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from app.models import Empleado
from app.forms import EmpleadoForm


class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'Empleado/listar.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Empleado.objects.all().order_by('nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Empleados'
        context['crear_url'] = reverse_lazy('app:crear_empleado')
        return context


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('app:listar_empleado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Empleado'
        context['listar_url'] = reverse_lazy('app:listar_empleado')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Empleado registrado correctamente.')
        return super().form_valid(form)


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('app:listar_empleado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Empleado'
        context['listar_url'] = reverse_lazy('app:listar_empleado')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Empleado actualizado correctamente.')
        return super().form_valid(form)


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'Empleado/eliminar.html'
    success_url = reverse_lazy('app:listar_empleado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Empleado'
        context['listar_url'] = reverse_lazy('app:listar_empleado')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Empleado eliminado correctamente.')
        return super().form_valid(form)