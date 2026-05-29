import threading

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
from django.utils import timezone

from app.models import Notificacion, Vehiculo, SeguimientoMantenimiento
from app.forms import NotificacionForm


# ── HELPER: enviar correo de notificación ─────────────────
def _enviar_correo_notificacion(cliente, vehiculo, tipo, mensaje):
    destinatarios = []
    if cliente and cliente.email:
        destinatarios.append(cliente.email)
    empresa_email = settings.EMAIL_HOST_USER
    if empresa_email not in destinatarios:
        destinatarios.append(empresa_email)
    if not destinatarios:
        return

    nombre_cliente = cliente.nombre if cliente else "Cliente"
    asunto = f"Recordatorio de mantenimiento — {vehiculo.placa} | ACERAUTOS"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:600px;margin:32px auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);">
    <div style="background:#1a1a1a;padding:28px 32px;text-align:center;border-bottom:4px solid #d32f2f;">
        <h1 style="margin:0;color:#fff;font-size:28px;font-weight:800;letter-spacing:3px;">ACERAUTOS</h1>
        <p style="margin:6px 0 0;color:#888;font-size:12px;letter-spacing:1px;text-transform:uppercase;">Centro Integral Automotriz</p>
    </div>
    <div style="padding:36px 32px;">
        <p style="margin:0 0 6px;font-size:13px;color:#888;text-transform:uppercase;letter-spacing:1px;">Estimado/a</p>
        <p style="margin:0 0 28px;font-size:22px;font-weight:700;color:#1a1a1a;">{nombre_cliente}</p>
        <p style="margin:0 0 24px;font-size:15px;color:#444;line-height:1.7;">Te informamos que el siguiente vehículo requiere atención:</p>
        <div style="background:#f8f8f8;border-radius:8px;padding:20px 24px;margin-bottom:24px;border-left:4px solid #d32f2f;">
            <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:6px 0;font-size:13px;color:#888;width:130px;">Placa</td><td style="padding:6px 0;font-size:14px;font-weight:700;color:#1a1a1a;">{vehiculo.placa}</td></tr>
                <tr><td style="padding:6px 0;font-size:13px;color:#888;">Vehículo</td><td style="padding:6px 0;font-size:14px;font-weight:600;color:#1a1a1a;">{vehiculo.marca.nombre} {vehiculo.modelo}</td></tr>
                <tr><td style="padding:6px 0;font-size:13px;color:#888;">Cliente</td><td style="padding:6px 0;font-size:14px;font-weight:600;color:#1a1a1a;">{nombre_cliente}</td></tr>
                <tr><td style="padding:6px 0;font-size:13px;color:#888;">Tipo de alerta</td><td style="padding:6px 0;font-size:14px;font-weight:700;color:#d32f2f;">{tipo}</td></tr>
            </table>
        </div>
        <div style="background:#fffbf0;border:1px solid #ffe0a0;border-radius:8px;padding:20px 24px;margin-bottom:28px;">
            <p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#b45309;text-transform:uppercase;letter-spacing:.5px;">⚠ Detalle del aviso</p>
            <p style="margin:0;font-size:15px;color:#333;line-height:1.7;">{mensaje}</p>
        </div>
        <p style="margin:0 0 28px;font-size:14px;color:#444;line-height:1.7;">Por favor <strong>comunícate con nosotros</strong> para agendar tu cita de mantenimiento.</p>
        <div style="background:#1a1a1a;border-radius:8px;padding:20px 24px;text-align:center;">
            <p style="margin:0 0 12px;font-size:13px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:1px;">Contáctanos</p>
            <p style="margin:0;font-size:13px;color:#aaa;line-height:1.9;">📞 +57 (8) 632-5678<br>💬 WhatsApp: +57 320 123 4567<br>📍 Yopal, Casanare — Colombia</p>
        </div>
    </div>
    <div style="background:#111;padding:20px 32px;text-align:center;border-top:1px solid #222;">
        <p style="margin:0 0 4px;font-size:12px;color:#555;"><span style="color:#d32f2f;font-weight:700;">ACERAUTOS</span> — Tu Confianza, Nuestro Compromiso</p>
        <p style="margin:0;font-size:11px;color:#444;">© 2026 ACERAUTOS. Todos los derechos reservados.</p>
    </div>
</div>
</body>
</html>"""

    texto = (
        f"Estimado/a {nombre_cliente},\n\n"
        f"El vehículo {vehiculo.placa} ({vehiculo.marca.nombre} {vehiculo.modelo}) "
        f"requiere atención.\n\nTipo de alerta: {tipo}\n\n{mensaje}\n\n"
        f"ACERAUTOS — Tu Confianza, Nuestro Compromiso"
    )

    try:
        print(f"[ACERAUTOS] Intentando enviar correo a: {destinatarios}")
        correo = EmailMultiAlternatives(
            subject=asunto, body=texto,
            from_email=settings.DEFAULT_FROM_EMAIL, to=destinatarios,
        )
        correo.attach_alternative(html, "text/html")
        correo.send()
        print(f"[ACERAUTOS] ✅ Correo enviado correctamente a: {destinatarios}")
    except Exception as e:
        print(f"[ACERAUTOS] ❌ Error enviando correo para {vehiculo.placa}: {e}")


# ── GENERAR NOTIFICACIONES AUTOMÁTICAS ────────────────────
def generar_notificaciones_automaticas():
    hoy = timezone.now().date()

    seguimientos = SeguimientoMantenimiento.objects.filter(
        activo=True,
        fecha_proximo_mantenimiento__isnull=False
    ).select_related('vehiculo', 'vehiculo__marca', 'vehiculo__cliente', 'tipo_servicio')

    for seg in seguimientos:
        v         = seg.vehiculo
        dias_rest = (seg.fecha_proximo_mantenimiento - hoy).days

        if dias_rest <= 0:
            dias_abs = abs(dias_rest)
            mensaje = f'El mantenimiento venció hace {dias_abs} día{"s" if dias_abs != 1 else ""}.'
            tipo    = 'Urgente'
            titulo  = f'Mantenimiento vencido — {v.placa}'
        elif dias_rest <= 7:
            mensaje = f'Faltan {dias_rest} día{"s" if dias_rest != 1 else ""} para el mantenimiento (fecha: {seg.fecha_proximo_mantenimiento.strftime("%d/%m/%Y")}).'
            tipo    = 'Urgente'
            titulo  = f'Mantenimiento próximo — {v.placa}'
        elif dias_rest <= 15:
            mensaje = f'Faltan {dias_rest} días para el mantenimiento (fecha: {seg.fecha_proximo_mantenimiento.strftime("%d/%m/%Y")}).'
            tipo    = 'Alerta'
            titulo  = f'Mantenimiento próximo — {v.placa}'
        else:
            continue

        # Si ya existe hoy con el mismo mensaje exacto → no hacer nada
        ya_existe = Notificacion.objects.filter(
            vehiculo=v,
            origen='SISTEMA',
            fecha=hoy,
            mensaje=mensaje,
        ).exists()

        if not ya_existe:
            # Marcar como leídas las notificaciones automáticas viejas
            # de días anteriores para no inflar el badge
            Notificacion.objects.filter(
                vehiculo=v,
                origen='SISTEMA',
            ).exclude(fecha=hoy).update(leido=True)

            # Borrar duplicados de hoy con mensaje desactualizado
            Notificacion.objects.filter(
                vehiculo=v,
                origen='SISTEMA',
                fecha=hoy,
            ).delete()

            # Crear la notificación nueva
            Notificacion.objects.create(
                tipo=tipo, origen='SISTEMA', titulo=titulo,
                vehiculo=v, mensaje=mensaje, leido=False,
            )

            # Enviar correo SOLO cuando se crea una notificación nueva
            if v.cliente:
                _enviar_correo_notificacion(v.cliente, v, tipo, mensaje)


# ── LISTADO ────────────────────────────────────────────────
class NotificacionListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'Notificacion/listar.html'
    context_object_name = 'object_list'
    login_url = 'login:login'

    def get(self, request, *args, **kwargs):
        # Ejecutar en background — la página carga inmediato
        # sin esperar a que se generen notificaciones ni se envíen correos
        t = threading.Thread(target=generar_notificaciones_automaticas)
        t.daemon = True
        t.start()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Notificacion.objects.all().order_by('leido', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Listado de Notificaciones'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        context['no_leidas'] = Notificacion.objects.filter(leido=False).count()
        return context


# ── CREAR ──────────────────────────────────────────────────
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
        if notificacion.vehiculo and notificacion.vehiculo.cliente:
            _enviar_correo_notificacion(
                notificacion.vehiculo.cliente, notificacion.vehiculo,
                notificacion.tipo, notificacion.mensaje,
            )
        messages.success(self.request, 'Notificación creada correctamente.')
        return redirect(self.success_url)


# ── EDITAR ─────────────────────────────────────────────────
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


# ── ELIMINAR ───────────────────────────────────────────────
class NotificacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Notificacion
    template_name = 'Notificacion/eliminar.html'
    success_url = reverse_lazy('app:listar_notificacion')
    login_url = 'login:login'

    def form_valid(self, form):
        messages.success(self.request, 'Notificación eliminada correctamente.')
        return super().form_valid(form)


# ── MARCAR UNA COMO LEÍDA ──────────────────────────────────
class MarcarLeidaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            notificacion = get_object_or_404(Notificacion, pk=pk)
            notificacion.leido = True
            notificacion.save(update_fields=['leido'])
            return JsonResponse({'ok': True, 'mensaje': 'Notificación marcada como leída.'})
        except Exception as e:
            return JsonResponse({'ok': False, 'mensaje': str(e)}, status=400)


# ── MARCAR TODAS COMO LEÍDAS ───────────────────────────────
class MarcarTodasLeidasView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            cantidad = Notificacion.objects.filter(leido=False).update(leido=True)
            return JsonResponse({'ok': True, 'cantidad': cantidad, 'mensaje': f'{cantidad} notificaciones marcadas como leídas.'})
        except Exception as e:
            return JsonResponse({'ok': False, 'mensaje': str(e)}, status=400)


# ── LIMPIAR NOTIFICACIONES ANTIGUAS ───────────────────────
class LimpiarNotificacionesAntiguasView(LoginRequiredMixin, View):
    def post(self, request):
        hoy = timezone.now().date()
        # Elimina notificaciones automáticas de días anteriores ya leídas
        Notificacion.objects.filter(
            origen='SISTEMA',
            leido=True,
            fecha__lt=hoy,
        ).delete()
        messages.success(request, 'Notificaciones antiguas eliminadas correctamente.')
        return redirect('app:listar_notificacion')


# ── API PARA EL NAVBAR ─────────────────────────────────────
@login_required(login_url='login:login')
def notificaciones_no_leidas(request):
    # Solo lee — no genera ni envía nada, respuesta inmediata
    qs_no_leidas = Notificacion.objects.filter(leido=False).order_by('-id')
    results = []
    for n in qs_no_leidas[:5]:
        subtitulo = ''
        if n.vehiculo:
            try:
                subtitulo = f'{n.vehiculo.placa} · {n.vehiculo.marca} {n.vehiculo.modelo}'
            except Exception:
                subtitulo = str(n.vehiculo)
        results.append({
            'tipo':      n.tipo,
            'titulo':    n.titulo if n.titulo else n.tipo,
            'mensaje':   n.mensaje,
            'subtitulo': subtitulo,
            'fecha':     n.fecha.strftime('%d/%m/%Y') if n.fecha else '',
        })
    return JsonResponse({
        'count':   qs_no_leidas.count(),
        'results': results,
    })