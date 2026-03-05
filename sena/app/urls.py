from django.urls import path
from .views.dashboard.views import DashboardView
from .views.Cliente.views import (ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView)
from .views.Vehiculo.views import (VehiculoListView, VehiculoCreateView, VehiculoUpdateView, VehiculoDeleteView)
from .views.Usuario.views import (UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView)
from .views.compra.views import (CompraListView, CompraCreateView, CompraUpdateView, CompraDeleteView)
from .views.Proveedor.views import (ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView)
from .views.VentasFactura.views import (VentasFacturaListView, VentasFacturaCreateView, VentasFacturaUpdateView, VentasFacturaDeleteView) 
from .views.Notificacion.views import (NotificacionListView, NotificacionCreateView, NotificacionUpdateView, NotificacionDeleteView) 
from .views.caja.views import (CajaListView, CajaCreateView, CajaUpdateView, CajaDeleteView) 
app_name = 'app'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('clientes/listar/', ClienteListView.as_view(), name='listar_clientes'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('clientes/editar/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),

    path('vehiculos/listar/', VehiculoListView.as_view(), name='listar_vehiculos'),
    path('vehiculos/crear/', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('vehiculos/editar/<int:pk>/', VehiculoUpdateView.as_view(), name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/', VehiculoDeleteView.as_view(), name='eliminar_vehiculo'),   

    path('compras/listar/', CompraListView.as_view(), name='lista_compras'),
    path('compras/crear/', CompraCreateView.as_view(), name='crear_compra'),
    path('compras/editar/<int:pk>/', CompraUpdateView.as_view(), name='editar_compra'),
    #path('compras/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='eliminar_compra'),

    # --- BLOQUE DE PROVEEDORES ---
    path('proveedor/listar/', ProveedorListView.as_view(), name='listar_proveedores'),
    path('proveedor/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),

    path('usuarios/listar/', UsuarioListView.as_view(), name='listar_usuario'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    
    
    path('ventas/listar/', VentasFacturaListView.as_view(), name='listar_factura'),
    path('ventas/crear/', VentasFacturaCreateView.as_view(), name='crear_factura'),
    path('ventas/editar/<int:pk>/', VentasFacturaUpdateView.as_view(), name='editar_factura'),
    path('ventas/eliminar/<int:pk>/', VentasFacturaDeleteView.as_view(), name='eliminar_factura'),
    
    path('notificaciones/listar/', NotificacionListView.as_view(), name='listar_notificacion'),
    path('notificaciones/crear/', NotificacionCreateView.as_view(), name='crear_notificacion'),
    path('notificaciones/editar/<int:pk>/', NotificacionUpdateView.as_view(), name='editar_notificacion'),
    path('notificaciones/eliminar/<int:pk>/', NotificacionDeleteView.as_view(), name='eliminar_notificacion'),
    
    
    path('caja/listar', CajaListView.as_view(), name='caja_listar'),
    path('caja/crear/', CajaCreateView.as_view(), name='caja_crear'),
    path('caja/editar/<int:pk>/', CajaUpdateView.as_view(), name='caja_editar'),
    path('caja/eliminar/<int:pk>/', CajaDeleteView.as_view(), name='caja_eliminar'),
]