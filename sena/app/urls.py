from django.urls import path
from app.views.Categorias.views import *
from app.views.Productos.views import *
from app.views.Vehiculo.views import *
from app.views.Cliente.views import *
from app.views.Notificacion.views import *

app_name = 'app'

urlpatterns = [

    
    path('listar_categorias/', CategoriasListView.as_view(), name='listar_categorias'),
    path('crear_categorias/', CategoriasCreateView.as_view(), name='crear_categorias'),
    path('editar_categorias/<int:pk>/', CategoriasUpdateView.as_view(), name='editar_categorias'),
    path('eliminar_categorias/<int:pk>/', CategoriasDeleteView.as_view(), name='eliminar_categorias'),

    
    path('listar_productos/', ProductosListView.as_view(), name='listar_productos'),
    path('crear_productos/', ProductosCreateView.as_view(), name='crear_productos'),
    path('editar_productos/<int:pk>/', ProductosUpdateView.as_view(), name='editar_productos'),
    path('eliminar_productos/<int:pk>/', ProductosDeleteView.as_view(), name='eliminar_productos'),

    
    path('listar_vehiculo/', VehiculoListView.as_view(), name='listar_vehiculo'),
    path('crear_vehiculo/', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('editar_vehiculo/<int:pk>/', VehiculoUpdateView.as_view(), name='editar_vehiculo'),
    path('eliminar_vehiculo/<int:pk>/', VehiculoDeleteView.as_view(), name='eliminar_vehiculo'),
    
    path('listar_cliente/', ClienteListView.as_view(), name='listar_cliente'),
    path('crear_cliente/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('editar_cliente/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),

    path('listar_notificacion/', NotificacionListView.as_view(), name='listar_notificacion'),
    path('crear_notificacion/', NotificacionCreateView.as_view(), name='crear_notificacion'),
    path('editar_notificacion/<int:pk>/', NotificacionUpdateView.as_view(), name='editar_notificacion'),
    path('eliminar_notificacion/<int:pk>/', NotificacionDeleteView.as_view(), name='eliminar_notificacion'),


]


    #path("vista2/", vista2, name='vista2'),
    #path("vista3/", vista3, name='vista3'),
