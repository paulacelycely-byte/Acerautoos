from django.urls import path
from .views.dashboard import views as vistas_dash
from .views.Cliente import views as vistas_cli
from .views.Vehiculo import views as vistas_veh
from .views.Usuario import views as vistas_usr
from .views.compra import views as vistas_compra
from .views.Proveedor import views as vistas_prov
from .views.Marca import views as vistas_marca
from .views.Producto import views as vistas_prod
from .views.VentasFactura import views as vistas_ventas
from .views.Notificacion import views as vistas_notif
from .views.caja import views as vistas_caja
from .views.tipo_servicio import views as vistas_tipo_serv
from .views.Orden_servicio import views as vistas_orden
from .views.DetalleOrdenProducto import views as vistas_detalles
from .views.CompatibilidadProducto import views as vistas_comp
from .views.factura import views as vistas_factura
from app import reportes as vistas_rep

app_name = 'app'

urlpatterns = [
    path('dashboard/', vistas_dash.DashboardView.as_view(), name='dashboard'),

    # --- CLIENTES ---
    path('clientes/listar/', vistas_cli.ClienteListView.as_view(), name='listar_clientes'),
    path('clientes/crear/', vistas_cli.ClienteCreateView.as_view(), name='crear_cliente'),
    path('clientes/editar/<int:pk>/', vistas_cli.ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', vistas_cli.ClienteDeleteView.as_view(), name='eliminar_cliente'),

    # --- VEHICULOS ---
    path('vehiculos/listar/', vistas_veh.VehiculoListView.as_view(), name='listar_vehiculos'),
    path('vehiculos/crear/', vistas_veh.VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('vehiculos/editar/<int:pk>/', vistas_veh.VehiculoUpdateView.as_view(), name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/', vistas_veh.VehiculoDeleteView.as_view(), name='eliminar_vehiculo'),

    # --- COMPRAS ---
    path('compras/listar/', vistas_compra.CompraListView.as_view(), name='lista_compras'),
    path('compras/crear/', vistas_compra.CompraCreateView.as_view(), name='crear_compra'),
    path('compras/editar/<int:pk>/', vistas_compra.CompraUpdateView.as_view(), name='editar_compra'),
    path('compras/eliminar/<int:pk>/', vistas_compra.CompraDeleteView.as_view(), name='eliminar_compra'),

    # --- PROVEEDORES ---
    path('proveedor/listar/', vistas_prov.ProveedorListView.as_view(), name='listar_proveedores'),
    path('proveedor/crear/', vistas_prov.ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedor/editar/<int:pk>/', vistas_prov.ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('proveedor/eliminar/<int:pk>/', vistas_prov.ProveedorDeleteView.as_view(), name='eliminar_proveedor'),

    # --- MARCAS ---
    path('marca/listar/', vistas_marca.MarcaListView.as_view(), name='listar_marca'),
    path('marca/crear/', vistas_marca.MarcaCreateView.as_view(), name='crear_marca'),
    path('marca/editar/<int:pk>/', vistas_marca.MarcaUpdateView.as_view(), name='editar_marca'),
    path('marca/eliminar/<int:pk>/', vistas_marca.MarcaDeleteView.as_view(), name='eliminar_marca'),
    path('marca/crear-ajax/', vistas_marca.crear_marca_ajax, name='crear_marca_ajax'),

    # --- COMPATIBILIDAD ---
    path('compatibilidad/listar/', vistas_comp.CompatibilidadListView.as_view(), name='listar_compatibilidad'),
    path('compatibilidad/crear/', vistas_comp.CompatibilidadCreateView.as_view(), name='crear_compatibilidad'),
    path('compatibilidad/editar/<int:pk>/', vistas_comp.CompatibilidadUpdateView.as_view(), name='editar_compatibilidad'),
    path('compatibilidad/eliminar/<int:pk>/', vistas_comp.CompatibilidadDeleteView.as_view(), name='eliminar_compatibilidad'),

    # --- USUARIOS ---
    path('usuarios/listar/', vistas_usr.UsuarioListView.as_view(), name='listar_usuario'),
    path('usuarios/crear/', vistas_usr.UsuarioCreateView.as_view(), name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', vistas_usr.UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', vistas_usr.UsuarioDeleteView.as_view(), name='eliminar_usuario'),

    # --- PRODUCTOS ---
    path('producto/listar/', vistas_prod.ProductoListView.as_view(), name='listar_producto'),
    path('producto/crear/', vistas_prod.ProductoCreateView.as_view(), name='crear_producto'),
    path('producto/editar/<int:pk>/', vistas_prod.ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/eliminar/<int:pk>/', vistas_prod.ProductoDeleteView.as_view(), name='eliminar_producto'),

    # --- VENTAS ---
    path('ventas/listar/', vistas_ventas.VentasFacturaListView.as_view(), name='listar_ventas'),
    path('ventas/crear/', vistas_ventas.VentasFacturaCreateView.as_view(), name='crear_venta'),
    path('ventas/editar/<int:pk>/', vistas_ventas.VentasFacturaUpdateView.as_view(), name='editar_venta'),
    path('ventas/eliminar/<int:pk>/', vistas_ventas.VentasFacturaDeleteView.as_view(), name='eliminar_venta'),

    # --- NOTIFICACIONES ---
    path('notificaciones/listar/', vistas_notif.NotificacionListView.as_view(), name='listar_notificacion'),
    path('notificaciones/crear/', vistas_notif.NotificacionCreateView.as_view(), name='crear_notificacion'),
    path('notificaciones/editar/<int:pk>/', vistas_notif.NotificacionUpdateView.as_view(), name='editar_notificacion'),
    path('notificaciones/eliminar/<int:pk>/', vistas_notif.NotificacionDeleteView.as_view(), name='eliminar_notificacion'),

    # --- CAJA ---
    path('caja/listar/', vistas_caja.CajaListView.as_view(), name='caja_listar'),
    path('caja/crear/', vistas_caja.CajaCreateView.as_view(), name='caja_crear'),
    path('caja/editar/<int:pk>/', vistas_caja.CajaUpdateView.as_view(), name='caja_editar'),
    path('caja/eliminar/<int:pk>/', vistas_caja.CajaDeleteView.as_view(), name='caja_eliminar'),

    # --- TIPO SERVICIO ---
    path('tipo_servicio/listar/', vistas_tipo_serv.TipoServicioListView.as_view(), name='tipo_servicio_list'),
    path('tipo_servicio/crear/', vistas_tipo_serv.TipoServicioCreateView.as_view(), name='tipo_servicio_create'),
    path('tipo_servicio/editar/<int:pk>/', vistas_tipo_serv.TipoServicioUpdateView.as_view(), name='tipo_servicio_update'),
    path('tipo_servicio/eliminar/<int:pk>/', vistas_tipo_serv.TipoServicioDeleteView.as_view(), name='tipo_servicio_delete'),

    # --- ORDEN SERVICIO ---
    path('orden_servicio/listar/', vistas_orden.OrdenServicioListView.as_view(), name='orden_servicio_list'),
    path('orden_servicio/crear/', vistas_orden.OrdenServicioCreateView.as_view(), name='orden_servicio_create'),
    path('orden_servicio/detalle/<int:pk>/', vistas_orden.OrdenServicioDetailView.as_view(), name='orden_servicio_detail'),  # ← NUEVO
    path('orden_servicio/editar/<int:pk>/', vistas_orden.OrdenServicioUpdateView.as_view(), name='orden_servicio_edit'),
    path('orden_servicio/eliminar/<int:pk>/', vistas_orden.OrdenServicioDeleteView.as_view(), name='orden_servicio_delete'),

    # --- DETALLES ORDEN ---
    path('detalles/', vistas_detalles.DetalleOrdenListView.as_view(), name='detalle_orden_list'),
    path('detalles/add/', vistas_detalles.DetalleOrdenCreateView.as_view(), name='detalle_orden_add'),
    path('detalles/edit/<int:pk>/', vistas_detalles.DetalleOrdenUpdateView.as_view(), name='detalle_orden_edit'),
    path('detalles/delete/<int:pk>/', vistas_detalles.DetalleOrdenDeleteView.as_view(), name='detalle_orden_delete'),

    # --- FACTURAS ---
    path('factura/listar/', vistas_factura.FacturaListView.as_view(), name='listar_factura'),
    path('factura/crear/', vistas_factura.FacturaCreateView.as_view(), name='crear_factura'),
    path('factura/detalle/<int:pk>/', vistas_factura.FacturaDetailView.as_view(), name='detalle_factura'),
    path('factura/eliminar/<int:pk>/', vistas_factura.FacturaDeleteView.as_view(), name='eliminar_factura'),
    path('factura/pagar/<int:pk>/', vistas_factura.PagarFacturaView.as_view(), name='pagar_factura'),

    # --- REPORTES PDF ---
    path('reportes/clientes/pdf/',    vistas_rep.ExportarClientesPDF.as_view(),    name='reporte_clientes_pdf'),
    path('reportes/vehiculos/pdf/',   vistas_rep.ExportarVehiculosPDF.as_view(),   name='reporte_vehiculos_pdf'),
    path('reportes/productos/pdf/',   vistas_rep.ExportarProductosPDF.as_view(),   name='reporte_productos_pdf'),
    path('reportes/proveedores/pdf/', vistas_rep.ExportarProveedoresPDF.as_view(), name='reporte_proveedores_pdf'),
    path('reportes/compras/pdf/',     vistas_rep.ExportarComprasPDF.as_view(),     name='reporte_compras_pdf'),
    path('reportes/caja/pdf/',        vistas_rep.ExportarCajaPDF.as_view(),        name='reporte_caja_pdf'),
    path('reportes/ordenes/pdf/',     vistas_rep.ExportarOrdenesPDF.as_view(),     name='reporte_ordenes_pdf'),
    path('reportes/facturas/pdf/',    vistas_rep.ExportarFacturasPDF.as_view(),    name='reporte_facturas_pdf'),

    # --- REPORTES EXCEL ---
    path('reportes/clientes/excel/',    vistas_rep.ExportarClientesExcel.as_view(),    name='reporte_clientes_excel'),
    path('reportes/vehiculos/excel/',   vistas_rep.ExportarVehiculosExcel.as_view(),   name='reporte_vehiculos_excel'),
    path('reportes/productos/excel/',   vistas_rep.ExportarProductosExcel.as_view(),   name='reporte_productos_excel'),
    path('reportes/proveedores/excel/', vistas_rep.ExportarProveedoresExcel.as_view(), name='reporte_proveedores_excel'),
    path('reportes/compras/excel/',     vistas_rep.ExportarComprasExcel.as_view(),     name='reporte_compras_excel'),
    path('reportes/caja/excel/',        vistas_rep.ExportarCajaExcel.as_view(),        name='reporte_caja_excel'),
    path('reportes/ordenes/excel/',     vistas_rep.ExportarOrdenesExcel.as_view(),     name='reporte_ordenes_excel'),
    path('reportes/facturas/excel/',    vistas_rep.ExportarFacturasExcel.as_view(),    name='reporte_facturas_excel'),
]