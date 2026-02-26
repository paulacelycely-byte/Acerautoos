from django.urls import path
from app.views.Ventas.views import Ventas_delete
from app.views.Entrada_vehiculo.views import *
from app.views.Ventas.views import *
from app.views.Usuario.views import *
from app.models import Ventas
from app.forms import VentasForm
from app.forms import Usuario
from app.forms import UsuarioForm
from app.views.Productos.views import *
from app.views.Vehiculo.views import *
from app.views.Cliente.views import *
from app.views.Notificacion.views import *
from django.urls import path, include
from .views.categorias.views import *
from .views.Proveedores.views import *
from .views.tipo_servicio.views import *
from .views.compra.views import *
from .views.factura.views import *
# Agregamos esta importación para el Dashboard
from .views.dashboard.views import DashboardView 

app_name = 'app'

urlpatterns = [
    # --- PANEL PRINCIPAL (DASHBOARD) ---
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # --- MÓDULO DE CATEGORÍAS ---
    path('listar_categorias/', CategoriaListView.as_view(), name='listar_categoria'),
    path('crear_categoria/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),

    #  ENTRADA VEHÍCULO
    path('listar_entrada_vehiculo/', Entrada_vehiculoListView.as_view(), name='listar_entrada_vehiculo'),
    path('crear_entrada_vehiculo/', Entrada_vehiculoCreateViews.as_view(), name='crear_entrada_vehiculo'),
    path('editar_entrada_vehiculo/<int:pk>/', Entrada_vehiculoUpdateView.as_view(), name='editar_entrada_vehiculo'),
    #path('eliminar_entrada_vehiculo/<int:pk>/', EntradaVehiculoDeleteView.as_view(), name='eliminar_entrada_vehiculo'),
    
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
    path('listar_categorias/', CategoriaListView.as_view(), name='listar_categorias'),
    path('crear_categorias/', CategoriaCreateView.as_view(), name='crear_categorias'),
    path('editar_categorias/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categorias'),
    path('eliminar_categorias/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categorias'),

    
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
        #path("vista2/", vista2, name='vista2'),
    #path("vista3/", vista3, name='vista3'),
    
    # --- MÓDULO DE PROVEEDORES ---
    path('proveedores/listar/', ProveedorListView.as_view(), name='listar_proveedores'),
    path('proveedores/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),
    
    # --- MÓDULO DE SERVICIOS ---
    path('tipo_servicio/listar/', TipoServicioListView.as_view(), name='listar_servicio'),
    path('tipo_servicio/crear/', TipoServicioCreateView.as_view(), name='crear_servicio'),
    path('tipo_servicio/editar/<int:pk>/', TipoServicioUpdateView.as_view(), name='editar_servicio'),
    path('tipo_servicio/eliminar/<int:pk>/', TipoServicioDeleteView.as_view(), name='eliminar_servicio'),

    # --- MÓDULO DE COMPRAS (CRUD COMPLETO) ---
    path('compra/listar/', CompraListView.as_view(), name='listar_compras'),
    path('compra/crear/', CompraCreateView.as_view(), name='crear_compra'),
    path('compra/editar/<int:pk>/', CompraUpdateView.as_view(), name='editar_compra'),
    path('compra/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='eliminar_compra'),

    # --- MÓDULO DE FACTURAS (SOLO CONSULTA) ---
    path('factura/listar/', FacturaListView.as_view(), name='listar_facturas'),
    path('factura/detalle/<int:pk>/', FacturaDetailView.as_view(), name='detalle_factura'),
    
    # --- MÓDULO DE LOGIN ---
    path('acceso/', include(('login.urls', 'login'), namespace='login')),
]



