from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from app.models import DetalleOrdenProducto
from app.forms import DetalleOrdenProductoForm

# ── MIXINS DE PROTECCIÓN ───────────────────────────────────

class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        # Solo el ADMIN puede Crear, Editar o Eliminar
        return self.request.user.is_authenticated and (
            self.request.user.cargo == 'ADMIN' or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(self.request, "Acceso denegado: Se requieren permisos de administrador.")
        return redirect('app:detalle_orden_list')

class AccesoLecturaTallerMixin(UserPassesTestMixin):
    def test_func(self):
        # REGLA SIMPLE: Si tiene un cargo (Mecánico, Empleado, Admin), puede ENTRAR A MIRAR
        # Esto evita errores por mayúsculas/minúsculas o tildes en el nombre del cargo
        return self.request.user.is_authenticated and self.request.user.cargo is not None

    def handle_no_permission(self):
        messages.error(self.request, "Debes ser parte del personal de Acerautos para ver esto.")
        return redirect('app:dashboard')


# 1. LISTADO (Ahora Pepe el mecánico ya puede entrar aquí)
class DetalleOrdenListView(LoginRequiredMixin, AccesoLecturaTallerMixin, ListView):
    model = DetalleOrdenProducto
    template_name = 'detalle/detalle_orden_list.html'
    context_object_name = 'detalles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Consulta de Productos en Orden'
        return context


# 2. CREAR DETALLE (Bloqueado para Pepe, solo tú puedes)
class DetalleOrdenCreateView(LoginRequiredMixin, SoloAdminMixin, CreateView):
    model = DetalleOrdenProducto
    form_class = DetalleOrdenProductoForm
    template_name = 'detalle/detalle_orden_add.html'
    success_url = reverse_lazy('app:detalle_orden_list')

    def form_valid(self, form):
        try:
            form.instance.full_clean()
            messages.success(self.request, "Producto registrado correctamente.")
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


# 3. EDITAR DETALLE (Bloqueado para Pepe)
class DetalleOrdenUpdateView(LoginRequiredMixin, SoloAdminMixin, UpdateView):
    model = DetalleOrdenProducto
    form_class = DetalleOrdenProductoForm
    template_name = 'detalle/detalle_orden_add.html'
    success_url = reverse_lazy('app:detalle_orden_list')


# 4. ELIMINAR DETALLE (Bloqueado para Pepe)
class DetalleOrdenDeleteView(LoginRequiredMixin, SoloAdminMixin, DeleteView):
    model = DetalleOrdenProducto
    template_name = 'detalle/detalle_orden_confirm_delete.html'
    success_url = reverse_lazy('app:detalle_orden_list')