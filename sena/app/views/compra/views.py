from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from ...models import Compra
from ...forms import CompraForm

class CompraListView(ListView):
    model = Compra
    template_name = 'Compra/listar.html' # Ajusta a tu ruta de template
    context_object_name = 'compras'

class CompraCreateView(SuccessMessageMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'Compra/crear.html'
    success_url = reverse_lazy('app:lista_compras')
    success_message = "Compra registrada y stock actualizado."

class CompraUpdateView(SuccessMessageMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'Compra/crear.html' # Usualmente usan el mismo que crear
    success_url = reverse_lazy('app:lista_compras')
    success_message = "Compra modificada exitosamente."

class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'Compra/eliminar.html'
    success_url = reverse_lazy('app:lista_compras')