from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.

class LoginFormView(LoginView):
    template_name = 'login/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('app:listar_categoria')


class LogoutFormView(LogoutView):
    next_page = reverse_lazy('login:login')
    


