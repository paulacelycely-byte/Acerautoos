from django.urls import path
from app.views.categorias.views import *

app_name = 'app'

urlpatterns = [
    path('listar_categorias/', categoriaListView.as_view(), name='listar_categoria'),
    path('crear_categoria/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
]

    #path("vista2/", vista2, name='vista2'),
    #path("vista3/", vista3, name='vista3'),
