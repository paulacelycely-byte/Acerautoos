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

from app.models import Notificacion, Vehiculo
from app.forms import NotificacionForm


# ── HELPER: enviar correo de notificación ─────────────────
def _enviar_correo_notificacion(cliente, vehiculo, tipo, mensaje):
    """
    Envía correo HTML al cliente (si tiene email) y siempre
    a la empresa (acerautos09@gmail.com).
    """
    destinatarios = []

    # Agregar correo del cliente si tiene
    if cliente and cliente.email:
        destinatarios.append(cliente.email)

    # Siempre agregar correo de la empresa
    empresa_email = settings.EMAIL_HOST_USER
    if empresa_email not in destinatarios:
        destinatarios.append(empresa_email)

    # Si no hay destinatarios (no debería pasar), salir
    if not destinatarios:
        return

    nombre_cliente = cliente.nombre if cliente else "Cliente"
    asunto = f"Recordatorio de mantenimiento — {vehiculo.placa} | ACERAUTOS"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:600px;margin:32px auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);">

    <!-- Header -->
    <div style="background:#1a1a1a;padding:28px 32px;text-align:center;border-bottom:4px solid #d32f2f;">
        <h1 style="margin:0;color:#fff;font-size:28px;font-weight:800;letter-spacing:3px;">ACERAUTOS</h1>
        <p style="margin:6px 0 0;color:#888;font-size:12px;letter-spacing:1px;text-transform:uppercase;">Centro Integral Automotriz</p>
    </div>

    <!-- Body -->
    <div style="padding:36px 32px;">
        <p style="margin:0 0 6px;font-size:13px;color:#888;text-transform:uppercase;letter-spacing:1px;">Estimado/a</p>
        <p style="margin:0 0 28px;font-size:22px;font-weight:700;color:#1a1a1a;">{nombre_cliente}</p>

        <p style="margin:0 0 24px;font-size:15px;color:#444;line-height:1.7;">
            Te informamos que el siguiente vehículo requiere atención:
        </p>

        <!-- Info vehículo -->
        <div style="background:#f8f8f8;border-radius:8px;padding:20px 24px;margin-bottom:24px;border-left:4px solid #d32f2f;">
            <table style="width:100%;border-collapse:collapse;">
                <tr>
                    <td style="padding:6px 0;font-size:13px;color:#888;width:130px;">Placa</td>
                    <td style="padding:6px 0;font-size:14px;font-weight:700;color:#1a1a1a;">{vehiculo.placa}</td>
                </tr>
                <tr>
                    <td style="padding:6px 0;font-size:13px;color:#888;">Vehículo</td>
                    <td style="padding:6px 0;font-size:14px;font-weight:600;color:#1a1a1a;">{vehiculo.marca.nombre} {vehiculo.modelo}</td>
                </tr>
                <tr>
                    <td style="padding:6px 0;font-size:13px;color:#888;">Cliente</td>
                    <td style="padding:6px 0;font-size:14px;font-weight:600;color:#1a1a1a;">{nombre_cliente}</td>
                </tr>
                <tr>
                    <td style="padding:6px 0;font-size:13px;color:#888;">Tipo de alerta</td>
                    <td style="padding:6px 0;font-size:14px;font-weight:700;color:#d32f2f;">{tipo}</td>
                </tr>
            </table>
        </div>

        <!-- Mensaje -->
        <div style="background:#fffbf0;border:1px solid #ffe0a0;border-radius:8px;padding:20px 24px;margin-bottom:28px;">
            <p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#b45309;text-transform:uppercase;letter-spacing:.5px;">⚠ Detalle del aviso</p>
            <p style="margin:0;font-size:15px;color:#333;line-height:1.7;">{mensaje}</p>
        </div>

        <p style="margin:0 0 28px;font-size:14px;color:#444;line-height:1.7;">
            Por favor <strong>comunícate con nosotros</strong> para agendar tu cita de mantenimiento a la brevedad posible.
        </p>

        <!-- Contacto -->
        <div style="background:#1a1a1a;border-radius:8px;padding:20px 24px;text-align:center;">
            <p style="margin:0 0 12px;font-size:13px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:1px;">Contáctanos</p>
            <p style="margin:0;font-size:13px;color:#aaa;line-height:1.9;">
                📞 +57 (8) 632-5678<br>
                💬 WhatsApp: +57 320 123 4567<br>
                📍 Yopal, Casanare — Colombia
            </p>
        </div>
    </div>

    <!-- Footer -->
    <div style="background:#111;padding:20px 32px;text-align:center;border-top:1px solid #222;">
        <p style="margin:0 0 4px;font-size:12px;color:#555;">
            <span style="color:#d32f2f;font-weight:700;">ACERAUTOS</span> — Tu Confianza, Nuestro Compromiso
        </p>
        <p style="margin:0;font-size:11px;color:#444;">© 2026 ACERAUTOS. Todos los derechos reservados.</p>
    </div>

</div>
</body>
</html>"""

    texto = (
        f"Estimado/a {nombre_cliente},\n\n"
        f"El vehículo {vehiculo.placa} ({vehiculo.marca.nombre} {vehiculo.modelo}) "
        f"del cliente {nombre_cliente} requiere atención.\n\n"
        f"Tipo de alerta: {tipo}\n\n"
        f"{mensaje}\n\n"
        f"Contáctanos:\n"
        f"Teléfono: +57 (8) 632-5678\n"
        f"WhatsApp: +57 320 123 4567\n\n"
        f"ACERAUTOS — Tu Confianza, Nuestro Compromiso"
    )

    try:
        correo = EmailMultiAlternatives(
            subject=asunto,
            body=texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=destinatarios,
        )
        correo.attach_alternative(html, "text/html")
        correo.send()
        print(f"[ACERAUTOS] Correo enviado a {destinatarios} para vehículo {vehiculo.placa}")
    except Exception as e:
        print(f"[ACERAUTOS] Error enviando correo para {vehiculo.placa}: {e}")


# ── GENERAR NOTIFICACIONES AUTOMÁTICAS ────────────────────
def generar_notificaciones_automaticas():
    """
    Revisa todos los vehículos y genera notificaciones automáticas
    si están próximos o vencidos en mantenimiento.
    Mensajes cortos y directos. Envía correo al cliente y a la empresa.
    """
    for v in Vehiculo.objects.select_related('marca', 'cliente').all():
        dias_rest = v.dias_restantes_mantenimiento()
        km_rest   = v.km_restantes_estimados()
        estado    = v.estado_mantenimiento()

        if estado == 'ok':
            continue

        tipo   = 'Mantenimiento'
        titulo = f'Mantenimiento próximo — {v.placa}'
        partes = []

        # ── Mensaje por FECHA ──
        if dias_rest is not None:
            if dias_rest <= 0:
                dias_abs = abs(dias_rest)
                partes.append(
                    f'El mantenimiento venció hace {dias_abs} día{"s" if dias_abs != 1 else ""}.'
                )
                tipo   = 'Urgente'
                titulo = f'Mantenimiento vencido — {v.placa}'
            elif dias_rest <= 7:
                partes.append(
                    f'Faltan {dias_rest} día{"s" if dias_rest != 1 else ""} para el mantenimiento '
                    f'(fecha límite: {v.fecha_proximo_mantenimiento.strftime("%d/%m/%Y")}).'
                )
                tipo = 'Urgente'
            elif dias_rest <= 15:
                partes.append(
                    f'Faltan {dias_rest} días para el mantenimiento '
                    f'(fecha límite: {v.fecha_proximo_mantenimiento.strftime("%d/%m/%Y")}).'
                )
                tipo = 'Alerta'
            elif dias_rest <= 30:
                partes.append(
                    f'Falta aproximadamente 1 mes para el mantenimiento '
                    f'(fecha límite: {v.fecha_proximo_mantenimiento.strftime("%d/%m/%Y")}).'
                )
            elif dias_rest <= 60:
                meses = round(dias_rest / 30)
                partes.append(
                    f'Faltan aproximadamente {meses} meses para el mantenimiento '
                    f'(fecha límite: {v.fecha_proximo_mantenimiento.strftime("%d/%m/%Y")}).'
                )

        # ── Mensaje por KM ──
        if km_rest is not None:
            if km_rest <= 0:
                partes.append(
                    f'El vehículo superó el límite de km '
                    f'(excedido por {abs(int(km_rest)):,} km).'
                )
                tipo   = 'Urgente'
                titulo = f'Mantenimiento vencido — {v.placa}'
            elif km_rest <= v.km_alerta_anticipacion:
                partes.append(
                    f'Faltan {int(km_rest):,} km para el próximo mantenimiento '
                    f'(próximo a los {v.km_proximo_mantenimiento:,} km).'
                )
                if tipo != 'Urgente':
                    tipo = 'Alerta'

        if not partes:
            continue

        mensaje = ' '.join(partes)

        # Evitar duplicados
        ya_existe = Notificacion.objects.filter(
            vehiculo=v,
            origen='SISTEMA',
            leido=False,
            titulo=titulo,
        ).exists()

        if not ya_existe:
            Notificacion.objects.create(
                tipo     = tipo,
                origen   = 'SISTEMA',
                titulo   = titulo,
                vehiculo = v,
                mensaje  = mensaje,
                leido    = False,
            )
            # Enviar correo al cliente Y a la empresa
            _enviar_correo_notificacion(v.cliente, v, tipo, mensaje)


# ── LISTADO DE NOTIFICACIONES ──────────────────────────────
class NotificacionListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'Notificacion/listar.html'
    context_object_name = 'object_list'
    login_url = 'login:login'

    def get(self, request, *args, **kwargs):
        generar_notificaciones_automaticas()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Notificacion.objects.all().order_by('leido', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Listado de Notificaciones'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        context['no_leidas'] = Notificacion.objects.filter(leido=False).count()
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

        if notificacion.vehiculo and notificacion.vehiculo.cliente:
            _enviar_correo_notificacion(
                notificacion.vehiculo.cliente,
                notificacion.vehiculo,
                notificacion.tipo,
                notificacion.mensaje,
            )

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
            return JsonResponse({'ok': True, 'cantidad': cantidad, 'mensaje': f'{cantidad} notificaciones marcadas como leídas.'})
        except Exception as e:
            return JsonResponse({'ok': False, 'mensaje': str(e)}, status=400)


# ── API PARA EL NAVBAR ─────────────────────────────────────
@login_required(login_url='login:login')
def notificaciones_no_leidas(request):
    generar_notificaciones_automaticas()

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
            'fecha':     n.fecha.strftime('%d/%m/%Y %H:%M') if n.fecha else '',
        })
    return JsonResponse({
        'count':   qs_no_leidas.count(),
        'results': results,
    })