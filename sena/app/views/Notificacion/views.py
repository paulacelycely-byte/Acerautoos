from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import Notificacion
from app.forms import NotificacionForm


class NotificacionListView(ListView):
    model = Notificacion
    template_name = 'Notificacion/listar.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Listado de Notificaciones'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        context['no_leidas'] = Notificacion.objects.filter(leido=False).count()
        return context


class NotificacionCreateView(CreateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Crear Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        context['es_editar']  = False
        return context

    def form_valid(self, form):
        notificacion = form.save(commit=False)
        notificacion.origen = 'ADMIN'
        notificacion.save()
        messages.success(self.request, 'Se creó correctamente la notificación.')
        return redirect(self.success_url)


class NotificacionUpdateView(UpdateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Editar Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        context['es_editar']  = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Notificación actualizada correctamente.')
        return super().form_valid(form)


class NotificacionDeleteView(DeleteView):
    model = Notificacion
    template_name = 'Notificacion/eliminar.html'
    success_url = reverse_lazy('app:listar_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Eliminar Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Notificación eliminada correctamente.')
        return super().delete(request, *args, **kwargs)


# ── Marcar una notificación como leída (AJAX POST) ────────
class MarcarLeidaView(View):
    def post(self, request, pk):
        notificacion = get_object_or_404(Notificacion, pk=pk)
        notificacion.leido = True
        notificacion.save(update_fields=['leido'])
        return JsonResponse({'ok': True, 'mensaje': 'Notificación marcada como leída.'})


# ── Marcar todas como leídas (AJAX POST) ──────────────────
class MarcarTodasLeidasView(View):
    def post(self, request):
        cantidad = Notificacion.objects.filter(leido=False).update(leido=True)
        sufijo_es = 'es' if cantidad != 1 else ''
        sufijo_as = 'as' if cantidad != 1 else 'a'
        return JsonResponse({
            'ok':      True,
            'cantidad': cantidad,
            'mensaje': f'{cantidad} notificación{sufijo_es} marcada{sufijo_as} como leída{sufijo_as}.'
        })


# ── Conteo de no leídas para el punto rojo del aside ──────
@login_required
def notificaciones_no_leidas(request):
    """
    GET /api/notificaciones/no-leidas/
    Devuelve {"count": N} — usado por aside.html para mostrar el punto rojo.
    """
    count = Notificacion.objects.filter(leido=False).count()
    return JsonResponse({'count': count})