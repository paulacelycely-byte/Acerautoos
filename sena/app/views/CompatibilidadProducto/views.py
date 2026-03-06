from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ...models import CompatibilidadProducto

# 1. LISTAR: Ver todas las compatibilidades registradas
class CompatibilidadListView(ListView):
    model = CompatibilidadProducto
    template_name = 'compatibilidadProducto/listar.html' # Ajusta según tu carpeta de templates
    context_object_name = 'compatibilidades'

# 2. CREAR: Registrar que un producto sirve para un vehículo
class CompatibilidadCreateView(CreateView):
    model = CompatibilidadProducto
    fields = ['producto', 'marca_vehiculo']
    template_name = 'compatibilidadProducto/crear.html'
    success_url = reverse_lazy('app:listar_compatibilidad')

# 3. EDITAR: Cambiar una relación si hubo un error
class CompatibilidadUpdateView(UpdateView):
    model = CompatibilidadProducto
    fields = ['producto', 'marca_vehiculo']
    template_name = 'compatibilidadProducto/crear.html' # Puedes reutilizar el mismo template
    success_url = reverse_lazy('app:listar_compatibilidad')

# 4. ELIMINAR: Borrar una relación
class CompatibilidadDeleteView(DeleteView):
    model = CompatibilidadProducto
    template_name = 'compatibilidadProducto/eliminar.html'
    success_url = reverse_lazy('app:listar_compatibilidad')