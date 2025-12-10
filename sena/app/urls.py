from django.urls import path
from app.views import *

app_name = 'app'
urlpatterns = [
    path("vista1/", vista1, name='vista1'),
    path("vista2/", vista2, name='vista2'),
    path("vista3/", vista3, name='vista3'),
]