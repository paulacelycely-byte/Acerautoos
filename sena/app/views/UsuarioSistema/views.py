from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from app.models import UsuarioSistema, OrdenServicio
from app.forms import UsuarioSistemaForm
from app.mixins import SoloSuperAdminMixin


class PerfilView(LoginRequiredMixin, View):
    login_url = 'login:login'

    def get(self, request):
        usuario = request.user
        ordenes_recientes = OrdenServicio.objects.filter(
            empleado=usuario
        ).select_related('vehiculo').order_by('-fecha')[:5] if hasattr(OrdenServicio, 'empleado') else []

        return render(request, 'UsuarioSistema/perfil.html', {
            'usuario'          : usuario,
            'ordenes_recientes': ordenes_recientes,
            'titulo'           : 'Mi Perfil',
        })


class UsuarioListView(SoloSuperAdminMixin, ListView):
    model               = UsuarioSistema
    template_name       = 'UsuarioSistema/listar.html'
    context_object_name = 'usuarios'
    login_url           = 'login:login'

    def get_queryset(self):
        return UsuarioSistema.objects.all().order_by('-is_superuser', 'cargo', 'username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Usuarios del Sistema'
        context['crear_url']  = reverse_lazy('app:crear_usuario')
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        return context


class UsuarioCreateView(SoloSuperAdminMixin, CreateView):
    model         = UsuarioSistema
    form_class    = UsuarioSistemaForm
    template_name = 'UsuarioSistema/crear.html'
    login_url     = 'login:login'

    # FIX — redirige a la orden si viene con ?next=orden
    def get_success_url(self):
        next_param = self.request.POST.get('next') or self.request.GET.get('next')
        if next_param == 'orden':
            return reverse_lazy('app:orden_servicio_create')
        return reverse_lazy('app:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Registro de Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        context['es_editar']  = False
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Usuario registrado correctamente.')
        return super().form_valid(form)


class UsuarioUpdateView(SoloSuperAdminMixin, UpdateView):
    model         = UsuarioSistema
    form_class    = UsuarioSistemaForm
    template_name = 'UsuarioSistema/crear.html'
    success_url   = reverse_lazy('app:listar_usuario')
    login_url     = 'login:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Editar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        context['es_editar']  = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado correctamente.')
        return super().form_valid(form)


class UsuarioDeleteView(SoloSuperAdminMixin, DeleteView):
    model         = UsuarioSistema
    template_name = 'UsuarioSistema/eliminar.html'
    success_url   = reverse_lazy('app:listar_usuario')
    login_url     = 'login:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Eliminar Usuario'
        context['listar_url'] = reverse_lazy('app:listar_usuario')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Usuario eliminado correctamente.')
        return super().form_valid(form)


class CambiarEstadoUsuarioView(SoloSuperAdminMixin, View):
    login_url = 'login:login'

    def post(self, request, pk):
        usuario = get_object_or_404(UsuarioSistema, pk=pk)
        if usuario.is_superuser:
            messages.error(request, 'No se puede desactivar un Super Admin.')
            return redirect('app:listar_usuario')
        usuario.is_active = not usuario.is_active
        usuario.save(update_fields=['is_active'])
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Usuario {usuario.username} {estado} correctamente.')
        return redirect('app:listar_usuario')