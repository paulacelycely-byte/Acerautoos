from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from app.models import UsuarioSistema, OrdenServicio, Empleado
from app.forms import UsuarioSistemaForm


class PerfilView(LoginRequiredMixin, View):
    """Vista de perfil del usuario logueado."""
    def get(self, request):
        usuario = request.user
        # Últimas órdenes asignadas si es mecánico (via empleado)
        ordenes_recientes = []
        try:
            empleado = Empleado.objects.get(correo=usuario.email)
            ordenes_recientes = OrdenServicio.objects.filter(
                empleado=empleado
            ).select_related('vehiculo', 'servicio').order_by('-fecha')[:5]
        except Empleado.DoesNotExist:
            pass

        return render(request, 'UsuarioSistema/perfil.html', {
            'usuario'          : usuario,
            'ordenes_recientes': ordenes_recientes,
            'titulo'           : 'Mi Perfil',
        })


class UsuarioSistemaListView(ListView):
    model = UsuarioSistema
    template_name = 'UsuarioSistema/listar.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return UsuarioSistema.objects.all().order_by('username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Listado de Usuarios'
        context['crear_url']  = reverse_lazy('app:crear_usuario')
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        return context


class UsuarioSistemaCreateView(CreateView):
    model = UsuarioSistema
    form_class = UsuarioSistemaForm
    template_name = 'UsuarioSistema/crear.html'
    success_url = reverse_lazy('app:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Registro de Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        context['action']     = 'add'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Se registró correctamente el usuario')
        return super().form_valid(form)


class UsuarioSistemaUpdateView(UpdateView):
    model = UsuarioSistema
    form_class = UsuarioSistemaForm
    template_name = 'UsuarioSistema/crear.html'
    success_url = reverse_lazy('app:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Editar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        context['action']     = 'edit'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Se editó correctamente el usuario')
        return super().form_valid(form)


class UsuarioSistemaDeleteView(DeleteView):
    model = UsuarioSistema
    template_name = 'UsuarioSistema/eliminar.html'
    success_url = reverse_lazy('app:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Eliminar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Se eliminó correctamente el usuario')
        return super().form_valid(form)


# ── Aliases ──
UsuarioListView   = UsuarioSistemaListView
UsuarioCreateView = UsuarioSistemaCreateView
UsuarioUpdateView = UsuarioSistemaUpdateView
UsuarioDeleteView = UsuarioSistemaDeleteView