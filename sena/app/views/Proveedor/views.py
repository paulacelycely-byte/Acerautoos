from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # ← Mixins para seguridad
from django.shortcuts import redirect # ← Necesario para la redirección de permisos
from django.http import JsonResponse
# IMPORTACIÓN ABSOLUTA
from app.models import Proveedor
from app.forms import ProveedorForm

# ── MIXIN DE PROTECCIÓN ───────────────────────────────────
class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        # Solo permite el acceso si el cargo es ADMIN o es superusuario
        return self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos de administrador para gestionar proveedores.")
        return redirect('app:dashboard')


# ================================
# LISTAR (Solo Admin)
# ================================
class ProveedorListView(LoginRequiredMixin, SoloAdminMixin, ListView):
    model = Proveedor
    template_name = 'Proveedor/listar.html' 
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Proveedores'
        context['crear_url'] = reverse_lazy('app:crear_proveedor')
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context


# ================================
# CREAR (Solo Admin)
# ================================
class ProveedorCreateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = 'Proveedor creado exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        context['action'] = 'add'
        return context


# ================================
# EDITAR (Solo Admin)
# ================================
class ProveedorUpdateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Proveedor/crear.html' 
    success_url = reverse_lazy('app:listar_proveedores')
    success_message = 'Proveedor actualizado exitosamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        context['action'] = 'edit'
        return context


# ================================
# ELIMINAR (Solo Admin)
# ================================
class ProveedorDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
    model = Proveedor
    template_name = 'Proveedor/eliminar.html'
    success_url = reverse_lazy('app:listar_proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Proveedor'
        context['listar_url'] = reverse_lazy('app:listar_proveedores')
        return context

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Proveedor eliminado exitosamente.')
        return self.delete(request, *args, **kwargs)
    
def validar_nit_proveedor(request):
    """
    GET /proveedor/validar-nit/?valor=123456789&exclude_pk=3
    Devuelve {"existe": true/false}
    """
    valor      = request.GET.get('valor', '').strip()
    exclude_pk = request.GET.get('exclude_pk', None)
    if not valor:
        return JsonResponse({'existe': False})
    qs = Proveedor.objects.filter(nit=valor)
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    return JsonResponse({'existe': qs.exists()})
 