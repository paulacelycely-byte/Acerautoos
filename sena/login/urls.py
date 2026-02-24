from django.urls import path
from login.views import loginFormView  # Importación específica para evitar errores

app_name = 'login'

urlpatterns = [
    path('', loginFormView.as_view(), name='login'),
    # Si aún no tienes la vista de logout, puedes comentar la siguiente línea con un #
    # path('logout/', logoutFormView.as_view(), name='logout'),
]