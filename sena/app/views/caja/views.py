from django.views.generic import ListView
from django.db.models import Sum
from app.models import Caja
from app.mixins import AdminRequeridoMixin


class CajaListView(AdminRequeridoMixin, ListView):
    model = Caja
    template_name = 'Caja/listar.html'
    context_object_name = 'object_list'
    login_url = 'login:login'

    def get_queryset(self):
        return Caja.objects.all().order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        total_ingresos = qs.filter(tipo='INGRESO').aggregate(t=Sum('monto'))['t'] or 0
        total_egresos  = qs.filter(tipo='EGRESO').aggregate(t=Sum('monto'))['t'] or 0

        context['titulo']            = 'Registro de Caja'
        context['total_ingresos']    = total_ingresos
        context['total_egresos']     = total_egresos
        context['saldo_caja']        = total_ingresos - total_egresos
        context['total_movimientos'] = qs.count()
        return context