from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class LoginFormView(LoginView):
    template_name = 'login/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('app:dashboard')  

class LogoutFormView(LogoutView):
    next_page = reverse_lazy('login:login')      