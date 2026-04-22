from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from app.models import Notificacion
from app.forms import NotificacionForm


# ── LISTADO DE NOTIFICACIONES ──────────────────────────────
class NotificacionListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'Notificacion/listar.html'
    context_object_name = 'object_list'
    login_url = 'login:login'

    def get_queryset(self):
        return Notificacion.objects.all().order_by('leido', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Listado de Notificaciones'
        context['crear_url']  = reverse_lazy('app:crear_notificacion')
        context['no_leidas']  = Notificacion.objects.filter(leido=False).count()
        return context


# ── CREAR NOTIFICACIÓN ─────────────────────────────────────
class NotificacionCreateView(LoginRequiredMixin, CreateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')
    login_url = 'login:login'

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

        # Enviar correo al cliente si hay vehículo asociado y tiene email
        if notificacion.vehiculo and notificacion.vehiculo.cliente:
            cliente = notificacion.vehiculo.cliente
            if cliente.email:
                asunto = f"Notificación sobre tu vehículo {notificacion.vehiculo.placa}"
                
                html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACERAUTOS - Notificación</title>
</head>
<body style="margin:0; padding:0; background-color:#f5f5f5; font-family:'Segoe UI', Arial, sans-serif;">
    <div style="max-width:650px; margin:0 auto; background-color:#ffffff;">
        
        <!-- ENCABEZADO ESTILO REPORTE -->
        <div style="padding:30px; text-align:center; border-bottom:3px solid #d32f2f;">
            <h1 style="margin:0; color:#d32f2f; font-size:32px; font-weight:bold; letter-spacing:2px;">ACERAUTOS</h1>
        </div>

        <!-- CONTENIDO PRINCIPAL -->
        <div style="padding:40px 30px; color:#333;">
            <p style="font-size:15px; margin:0 0 20px 0; color:#1a1a1a;">Estimado/a <strong>{cliente.nombre}</strong>,</p>
            
            <p style="font-size:14px; line-height:1.8; color:#444; margin:0 0 25px 0;">
                Queremos informarte que tu vehículo requiere atención:
            </p>

            <!-- TABLA CON INFORMACIÓN DEL VEHÍCULO (ESTILO REPORTE) -->
            <table width="100%" style="border-collapse:collapse; margin:20px 0; border:1px solid #ddd;">
                <tr style="background-color:#1a1a1a; color:white;">
                    <td style="padding:12px 15px; font-weight:bold; font-size:13px; text-transform:uppercase;">Vehículo</td>
                    <td style="padding:12px 15px; font-weight:bold; font-size:13px; text-transform:uppercase;">Marca/Modelo</td>
                    <td style="padding:12px 15px; font-weight:bold; font-size:13px; text-transform:uppercase;">Tipo de Alerta</td>
                </tr>
                <tr style="background-color:#f9f9f9;">
                    <td style="padding:14px 15px; border-right:1px solid #ddd; color:#1a1a1a; font-weight:600; font-size:14px;">{notificacion.vehiculo.placa}</td>
                    <td style="padding:14px 15px; border-right:1px solid #ddd; color:#1a1a1a; font-weight:600; font-size:14px;">{notificacion.vehiculo.marca.nombre} {notificacion.vehiculo.modelo}</td>
                    <td style="padding:14px 15px; color:#d32f2f; font-weight:bold; font-size:14px;">⚠ {notificacion.tipo}</td>
                </tr>
            </table>

            <!-- MENSAJE DETALLADO -->
            <div style="background-color:#fff8f0; padding:20px; margin:25px 0; border-radius:5px; border:1px solid #ffdbcc;">
                <p style="margin:0; font-size:14px; line-height:1.7; color:#333;">
                    <strong>Descripción:</strong><br>
                    {notificacion.mensaje}
                </p>
            </div>

            <!-- LLAMADA A LA ACCIÓN -->
            <p style="font-size:14px; line-height:1.8; color:#444; margin:25px 0;">
                Por favor <strong>comunícate con nosotros</strong> para agendar tu cita y garantizar el óptimo funcionamiento de tu vehículo.
            </p>

            <!-- DATOS DE CONTACTO -->
            <div style="background-color:#f0f0f0; padding:20px; margin:25px 0; border-radius:5px; text-align:center;">
                <p style="margin:0 0 10px 0; font-size:14px; font-weight:bold; color:#1a1a1a;">Contáctanos:</p>
                <p style="margin:5px 0; font-size:13px; color:#444;">
                    <strong>Teléfono:</strong> +57 (8) 632-5678<br>
                    <strong>WhatsApp:</strong> +57 320 123 4567<br>
                    <strong>Ubicación:</strong> Yopal, Casanare - Colombia
                </p>
            </div>
        </div>

        <!-- FOOTER -->
        <div style="background-color:#1a1a1a; color:#888; padding:25px; text-align:center; border-top:3px solid #d32f2f;">
            <p style="margin:0 0 8px; font-size:12px; font-weight:bold;">
                <span style="color:#d32f2f;">ACERAUTOS</span> - Tu Confianza, Nuestro Compromiso
            </p>
            <p style="margin:0; font-size:10px; color:#666;">
                © 2026 ACERAUTOS. Todos los derechos reservados.
            </p>
        </div>
    </div>
</body>
</html>
                """
                
                texto = (
                    f"Estimado/a {cliente.nombre},\n\n"
                    f"{notificacion.mensaje}\n\n"
                    f"Vehículo: {notificacion.vehiculo.placa}\n\n"
                    f"Te recomendamos que agendes tu cita lo antes posible.\n\n"
                    f"ACERAUTOS - Tu Confianza, Nuestro Compromiso"
                )
                
                try:
                    correo = EmailMultiAlternatives(
                        subject    = asunto,
                        body       = texto,
                        from_email = settings.DEFAULT_FROM_EMAIL,
                        to         = [cliente.email],
                    )
                    correo.attach_alternative(html, "text/html")
                    correo.send()
                except Exception as e:
                    print(f"Error enviando correo: {e}")

        messages.success(self.request, 'Notificación creada correctamente.')
        return redirect(self.success_url)


# ── EDITAR NOTIFICACIÓN ─────────────────────────────────────
class NotificacionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificacion')
    success_message = "Notificación actualizada correctamente."
    login_url = 'login:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Editar Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificacion')
        context['es_editar']  = True
        return context


# ── ELIMINAR NOTIFICACIÓN ───────────────────────────────────
class NotificacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Notificacion
    template_name = 'Notificacion/eliminar.html'
    success_url = reverse_lazy('app:listar_notificacion')
    login_url = 'login:login'

    def form_valid(self, form):
        messages.success(self.request, 'Notificación eliminada correctamente.')
        return super().form_valid(form)


# ── MARCAR UNA COMO LEÍDA (AJAX) ───────────────────────────
class MarcarLeidaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            notificacion = get_object_or_404(Notificacion, pk=pk)
            notificacion.leido = True
            notificacion.save(update_fields=['leido'])
            return JsonResponse({'ok': True, 'mensaje': 'Notificación marcada como leída.'})
        except Exception as e:
            return JsonResponse({'ok': False, 'mensaje': str(e)}, status=400)


# ── MARCAR TODAS COMO LEÍDAS (AJAX) ────────────────────────
class MarcarTodasLeidasView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            cantidad = Notificacion.objects.filter(leido=False).update(leido=True)
            msg = f'{cantidad} notificaciones marcadas como leídas.'
            return JsonResponse({'ok': True, 'cantidad': cantidad, 'mensaje': msg})
        except Exception as e:
            return JsonResponse({'ok': False, 'mensaje': str(e)}, status=400)


# ── API PARA EL NAVBAR ─────────────────────────────────────
@login_required(login_url='login:login')
def notificaciones_no_leidas(request):
    qs_no_leidas = Notificacion.objects.filter(leido=False).order_by('-id')
    results = []
    for n in qs_no_leidas[:5]:
        results.append({
            'tipo':    n.get_tipo_display() if hasattr(n, 'get_tipo_display') else "ALERTA",
            'mensaje': n.mensaje,
        })
    return JsonResponse({
        'count':   qs_no_leidas.count(),
        'results': results,
    })