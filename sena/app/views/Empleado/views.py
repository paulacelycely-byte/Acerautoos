from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

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
        context['titulo']    = 'Listado de Empleados'
        context['crear_url'] = reverse_lazy('app:crear_empleado')
        return context


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('app:listar_empleado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Registrar Empleado'
        context['listar_url']= reverse_lazy('app:listar_empleado')
        context['es_editar'] = False
        context['next']      = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Empleado registrado correctamente.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('app:listar_empleado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Editar Empleado'
        context['listar_url']= reverse_lazy('app:listar_empleado')
        context['es_editar'] = True
        context['next']      = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        self.object = form.save()
        next_param = self.request.POST.get('next', '')
        messages.success(self.request, 'Empleado actualizado correctamente.')
        if next_param == 'orden':
            return redirect(reverse_lazy('app:orden_servicio_create'))
        return redirect(self.success_url)


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'Empleado/eliminar.html'
    success_url = reverse_lazy('app:listar_empleado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Eliminar Empleado'
        context['listar_url']= reverse_lazy('app:listar_empleado')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Empleado eliminado correctamente.')
        return super().form_valid(form)