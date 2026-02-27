from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html' # Este es tu panel azul