from django.urls import path
from app.views.Ventas.views import Ventas_delete
from app.views.Categorias.views import *
from app.views.Entrada_vehiculo.views import *
from app.views.Ventas.views import *
from app.views.Usuario.views import *
from app.models import Ventas
from app.forms import VentasForm
from app.forms import Usuario
from app.forms import UsuarioForm

app_name = 'app'

urlpatterns = [

    # CATEGORÍAS
    path('listar_categorias/', categoriaListView.as_view(), name='listar_categoria'),
    path('crear_categoria/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),

    #  ENTRADA VEHÍCULO
    path('listar_entrada_vehiculo/', Entrada_vehiculoListView.as_view(), name='listar_entrada_vehiculo'),
    path('crear_entrada_vehiculo/', Entrada_vehiculoCreateViews.as_view(), name='crear_entrada_vehiculo'),
    path('editar_entrada_vehiculo/<int:pk>/', Entrada_vehiculoUpdateView.as_view(), name='editar_entrada_vehiculo'),
    path('eliminar_entrada_vehiculo/<int:pk>/', EntradaVehiculoDeleteView.as_view(), name='eliminar_entrada_vehiculo'),
    
    #  Ventas
    path('listar_Ventas/', VentasListView.as_view(), name='listar_Ventas'),
    path('crear_Ventas/', VentasCreateView.as_view(), name='crear_Ventas'),
    path('editar_Ventas/<int:pk>/', VentasUpdateView.as_view(), name='editar_Ventas'),
    path('eliminar_Ventas/<int:pk>/',Ventas_delete.as_view(), name='eliminar_Ventas'),

    #  Usuario
    path('listar_Usuario/', UsuarioListView.as_view(), name='listar_Usuario'),
    path('crear_Usuario/', UsuarioCreateView.as_view(), name='crear_Usuario'),
    path('editar_Usuario/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_Usuario'),
    path('eliminar_Usuario/<int:pk>/',UsuarioDeleteView.as_view(), name='eliminar_Usuario'),
]




