from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
class AyudaView(View):
    def get(self, request):
        context = {
            'titulo': 'Centro de Ayuda',
        }
        return render(request, 'ayuda/ayuda.html', context)