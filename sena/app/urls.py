from django.urls import path
from .views.dashboard.views import DashboardView
from .views.Cliente.views import (
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView)
from .views.Vehiculo.views import (
    VehiculoListView, VehiculoCreateView, VehiculoUpdateView, VehiculoDeleteView)
from .views.Usuario.views import (
    UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView)
from .views.compra.views import (
    CompraListView, CompraCreateView, CompraUpdateView, CompraDeleteView)
from .views.Proveedor.views import (
    ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView)
from .views.tipo_servicio.views import (
    TipoServicioListView, TipoServicioCreateView, TipoServicioUpdateView, TipoServicioDeleteView)
from .views.Orden_servicio.views import (
    OrdenServicioListView, OrdenServicioCreateView, OrdenServicioUpdateView, OrdenServicioDeleteView)
from .views.DetalleOrdenProducto.views import (DetalleOrdenListView, DetalleOrdenCreateView,
                                               DetalleOrdenUpdateView, DetalleOrdenDeleteView)
app_name = 'app'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('clientes/listar/', ClienteListView.as_view(), name='listar_clientes'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('clientes/editar/<int:pk>/',
         ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/',
         ClienteDeleteView.as_view(), name='eliminar_cliente'),

    path('vehiculos/listar/', VehiculoListView.as_view(), name='listar_vehiculos'),
    path('vehiculos/crear/', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('vehiculos/editar/<int:pk>/',
         VehiculoUpdateView.as_view(), name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/',
         VehiculoDeleteView.as_view(), name='eliminar_vehiculo'),

    path('compras/listar/', CompraListView.as_view(), name='lista_compras'),
    path('compras/crear/', CompraCreateView.as_view(), name='crear_compra'),
    path('compras/editar/<int:pk>/',
         CompraUpdateView.as_view(), name='editar_compra'),
    # path('compras/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='eliminar_compra'),

    # --- BLOQUE DE PROVEEDORES ---
    path('proveedor/listar/', ProveedorListView.as_view(),
         name='listar_proveedores'),
    path('proveedor/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedor/editar/<int:pk>/',
         ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('proveedor/eliminar/<int:pk>/',
         ProveedorDeleteView.as_view(), name='eliminar_proveedor'),

    path('usuarios/listar/', UsuarioListView.as_view(), name='listar_usuario'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('usuarios/editar/<int:pk>/',
         UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/',
         UsuarioDeleteView.as_view(), name='eliminar_usuario'),

    path('tipo_servicio/listar/', TipoServicioListView.as_view(),
         name='tipo_servicio_list'),
    path('tipo_servicio/crear/', TipoServicioCreateView.as_view(),
         name='tipo_servicio_create'),
    path('tipo_servicio/editar/<int:pk>/',
         TipoServicioUpdateView.as_view(), name='tipo_servicio_update'),
    path('tipo_servicio/eliminar/<int:pk>/',
         TipoServicioDeleteView.as_view(), name='tipo_servicio_delete'),
    path('detalles/', DetalleOrdenListView.as_view(), name='detalle_orden_list'),
    path('detalles/add/', DetalleOrdenCreateView.as_view(),
         name='detalle_orden_add'),
    path('detalles/edit/<int:pk>/', DetalleOrdenUpdateView.as_view(),
         name='detalle_orden_edit'),
    path('detalles/delete/<int:pk>/', DetalleOrdenDeleteView.as_view(),
         name='detalle_orden_delete'),
]
