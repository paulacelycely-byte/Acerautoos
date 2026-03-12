from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.models import Marca
from app.forms import MarcaForm


# ================================
# LISTAR
# ================================
class MarcaListView(ListView):
    model = Marca
    template_name = 'Marca/listar.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Marca.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Marca'
        context['crear_url'] = reverse_lazy('app:crear_marca')
        context['listar_url'] = reverse_lazy('app:listar_marca')
        return context


# ================================
# CREAR
# ================================
class MarcaCreateView(SuccessMessageMixin, CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear.html'
    success_url = reverse_lazy('app:listar_marca')
    success_message = 'Marca creada exitosamente.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Marca'
        context['listar_url'] = reverse_lazy('app:listar_marca')
        return context


# ================================
# EDITAR
# ================================
class MarcaUpdateView(SuccessMessageMixin, UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear.html'
    success_url = reverse_lazy('app:listar_marca')
    success_message = 'Marca actualizada exitosamente.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Marca'
        context['listar_url'] = reverse_lazy('app:listar_marca')
        return context


# ================================
# ELIMINAR / DESACTIVAR
# ================================
class MarcaDeleteView(View):
    def get(self, request, pk):
        marca = get_object_or_404(Marca, pk=pk)
        return render(request, 'Marca/eliminar.html', {
            'object': marca,
            'titulo': 'Eliminar Marca',
            'listar_url': reverse_lazy('app:listar_marca')
        })

    def post(self, request, pk):
        marca = get_object_or_404(Marca, pk=pk)
        accion = request.POST.get("accion")

        if accion == "desactivar":
            marca.estado = False
            marca.save()
            messages.success(request, "Marca desactivada correctamente.")
        else:
            try:
                marca.delete()
                messages.success(request, "Marca eliminada definitivamente.")
            except ProtectedError:
                messages.error(request,
                    f"No se puede eliminar '{marca.nombre}' porque está siendo usada "
                    f"por vehículos o productos registrados en el sistema. "
                    f"Primero elimina o reasigna esos registros."
                )
                return redirect('app:listar_marca')

        return redirect('app:listar_marca')


# ================================
# CREAR MARCA AJAX (modal desde vehículos)
# ================================
@require_POST
def crear_marca_ajax(request):
    nombre = request.POST.get('nombre', '').strip()
    pais   = request.POST.get('pais_origen', '').strip()
    desc   = request.POST.get('descripcion', '').strip()

    if not nombre:
        return JsonResponse({'success': False, 'error': 'El nombre es obligatorio.'})
    if len(nombre) < 2:
        return JsonResponse({'success': False, 'error': 'El nombre debe tener al menos 2 caracteres.'})
    if Marca.objects.filter(nombre__iexact=nombre).exists():
        return JsonResponse({'success': False, 'error': f'La marca "{nombre}" ya existe en el sistema.'})

    marca = Marca.objects.create(
        nombre=nombre,
        pais_origen=pais or None,
        descripcion=desc or None
    )
    return JsonResponse({'success': True, 'id': marca.pk, 'nombre': marca.nombre})