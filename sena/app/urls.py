from django.urls import path
from .views.dashboard.views import DashboardView
from .views.Cliente.views import (
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView)
from .views.Vehiculo.views import (
    VehiculoListView, VehiculoCreateView, VehiculoUpdateView, VehiculoDeleteView)
from .views.Usuario.views import (
    UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView)
from .views.compra.views import (
    CompraListView, CompraCreateView, CompraUpdateView)
from .views.Proveedor.views import (
    ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView)
from .views.Marca.views import (
    MarcaListView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView)
from .views.Producto.views import (
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView)
from .views.Proveedor.views import (
    ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView)
from .views.VentasFactura.views import (
    VentasFacturaListView, VentasFacturaCreateView, VentasFacturaUpdateView, VentasFacturaDeleteView)
from .views.Notificacion.views import (
    NotificacionListView, NotificacionCreateView, NotificacionUpdateView, NotificacionDeleteView)
from .views.caja.views import (
    CajaListView, CajaCreateView, CajaUpdateView, CajaDeleteView)
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

    # --- CLIENTES ---
    path('clientes/listar/', ClienteListView.as_view(), name='listar_clientes'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('clientes/editar/<int:pk>/',
         ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/',
         ClienteDeleteView.as_view(), name='eliminar_cliente'),

    # --- VEHICULOS ---
    path('vehiculos/listar/', VehiculoListView.as_view(), name='listar_vehiculos'),
    path('vehiculos/crear/', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('vehiculos/editar/<int:pk>/',
         VehiculoUpdateView.as_view(), name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/',
         VehiculoDeleteView.as_view(), name='eliminar_vehiculo'),

    # --- COMPRAS ---
    path('compras/listar/', CompraListView.as_view(), name='lista_compras'),
    path('compras/crear/', CompraCreateView.as_view(), name='crear_compra'),
    path('compras/editar/<int:pk>/',
         CompraUpdateView.as_view(), name='editar_compra'),

    # --- PROVEEDORES ---
    path('proveedor/listar/', ProveedorListView.as_view(),
         name='listar_proveedores'),
    path('proveedor/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedor/editar/<int:pk>/',
         ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('proveedor/eliminar/<int:pk>/',
         ProveedorDeleteView.as_view(), name='eliminar_proveedor'),

    # --- MARCAS ---
    path('marca/listar/', MarcaListView.as_view(), name='listar_marca'),
    path('marca/crear/', MarcaCreateView.as_view(), name='crear_marca'),
    path('marca/editar/<int:pk>/', MarcaUpdateView.as_view(), name='editar_marca'),
    path('marca/eliminar/<int:pk>/',
         MarcaDeleteView.as_view(), name='eliminar_marca'),

    # --- USUARIOS ---
    path('usuarios/listar/', UsuarioListView.as_view(), name='listar_usuario'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('usuarios/editar/<int:pk>/',
         UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/',
         UsuarioDeleteView.as_view(), name='eliminar_usuario'),

    # --- PRODUCTOS ---
    path('producto/listar/', ProductoListView.as_view(), name='listar_producto'),
    path('producto/crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('producto/editar/<int:pk>/',
         ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/eliminar/<int:pk>/',
         ProductoDeleteView.as_view(), name='eliminar_producto'),



    path('ventas/listar/', VentasFacturaListView.as_view(), name='listar_factura'),
    path('ventas/crear/', VentasFacturaCreateView.as_view(), name='crear_factura'),
    path('ventas/editar/<int:pk>/',
         VentasFacturaUpdateView.as_view(), name='editar_factura'),
    path('ventas/eliminar/<int:pk>/',
         VentasFacturaDeleteView.as_view(), name='eliminar_factura'),

    path('notificaciones/listar/', NotificacionListView.as_view(),
         name='listar_notificacion'),
    path('notificaciones/crear/', NotificacionCreateView.as_view(),
         name='crear_notificacion'),
    path('notificaciones/editar/<int:pk>/',
         NotificacionUpdateView.as_view(), name='editar_notificacion'),
    path('notificaciones/eliminar/<int:pk>/',
         NotificacionDeleteView.as_view(), name='eliminar_notificacion'),


    path('caja/listar', CajaListView.as_view(), name='caja_listar'),
    path('caja/crear/', CajaCreateView.as_view(), name='caja_crear'),
    path('caja/editar/<int:pk>/', CajaUpdateView.as_view(), name='caja_editar'),
    path('caja/eliminar/<int:pk>/', CajaDeleteView.as_view(), name='caja_eliminar'),

    path('tipo_servicio/listar/', TipoServicioListView.as_view(),
         name='tipo_servicio_list'),
    path('tipo_servicio/crear/', TipoServicioCreateView.as_view(),
         name='tipo_servicio_create'),
    path('tipo_servicio/editar/<int:pk>/',
         TipoServicioUpdateView.as_view(), name='tipo_servicio_update'),
    path('tipo_servicio/eliminar/<int:pk>/',
         TipoServicioDeleteView.as_view(), name='tipo_servicio_delete'),
    path('orden_servicio/',OrdenServicioListView.as_view(),name='orden_servicio_list'),
    path('orden_servicio/crear',OrdenServicioCreateView.as_view(),name='orden_servicio_create'),
    path('orden_servicio/editar/<int:pk>/',OrdenServicioUpdateView.as_view(),name='orden_servicio_edit'),
    path('orden_servicio/eliminar/<int:pk>/',OrdenServicioDeleteView.as_view(),name='orden_servicio_delete'),
    path('detalles/', DetalleOrdenListView.as_view(), name='detalle_orden_list'),
    path('detalles/add/', DetalleOrdenCreateView.as_view(),
         name='detalle_orden_add'),
    path('detalles/edit/<int:pk>/', DetalleOrdenUpdateView.as_view(),
         name='detalle_orden_edit'),
    path('detalles/delete/<int:pk>/', DetalleOrdenDeleteView.as_view(),
         name='detalle_orden_delete'),
]
