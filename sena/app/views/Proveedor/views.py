from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from app.models import Proveedor
from app.forms import ProveedorForm


# ── Mixin 1: Solo ADMIN ──────────────────────────────────────────
class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos de administrador para gestionar proveedores.")
        return redirect('app:dashboard')

# ── Mixin 2: ADMIN o MECANICO ────────────────────────────────────
class AdminOMecanicoMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.cargo in ('ADMIN', 'MECANICO') or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a este módulo.")
        return redirect('app:dashboard')


# ── LISTAR — Mecánico puede ver ──────────────────────────────────
class ProveedorListView(LoginRequiredMixin, AdminOMecanicoMixin, ListView):
    model = Proveedor
    template_name = 'Proveedor/listar.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Listado de Proveedores'
        context['crear_url']  = reverse_lazy('app:crear_proveedor')
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context


# ── CREAR — Solo Admin ────────────────────────────────────────────
class ProveedorCreateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = 'Proveedor creado exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Registro de Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        context['action']     = 'add'
        return context


# ── EDITAR — Solo Admin ───────────────────────────────────────────
class ProveedorUpdateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = 'Proveedor actualizado exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Editar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        context['action']     = 'edit'
        return context


# ── ELIMINAR — Solo Admin ─────────────────────────────────────────
class ProveedorDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
    model = Proveedor
    template_name = 'Proveedor/eliminar.html'
    success_url = reverse_lazy('app:listar_proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Eliminar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Proveedor eliminado exitosamente.')
        return self.delete(request, *args, **kwargs)