from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins de seguridad
from django.shortcuts import redirect

from ...models import Compra
from ...forms import CompraForm


# ── MIXIN DE PROTECCIÓN (Acerautos) ───────────────────────────
class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        # Solo permite el acceso si el cargo es ADMIN o es superusuario
        return self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos de administrador para gestionar las compras.")
        return redirect('app:dashboard')


# 1. LISTADO DE COMPRAS (Solo Admin)
class CompraListView(LoginRequiredMixin, SoloAdminMixin, ListView):
    model = Compra
    template_name = 'Compra/listar.html' 
    context_object_name = 'compras'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Historial de Compras'
        return context


# 2. REGISTRAR COMPRA (Solo Admin)
class CompraCreateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'Compra/crear.html'
    success_url = reverse_lazy('app:lista_compras')
    success_message = "Compra registrada y stock actualizado correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nueva Compra'
        return context


# 3. MODIFICAR COMPRA (Solo Admin)
class CompraUpdateView(LoginRequiredMixin, SoloAdminMixin, SuccessMessageMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'Compra/crear.html'
    success_url = reverse_lazy('app:lista_compras')
    success_message = "Compra modificada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Registro de Compra'
        return context


# 4. ELIMINAR COMPRA (Solo Admin)
class CompraDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
    model = Compra
    template_name = 'Compra/eliminar.html'
    success_url = reverse_lazy('app:lista_compras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Registro de Compra'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El registro de compra ha sido eliminado.")
        return super().delete(request, *args, **kwargs)