from django.urls import path, include
from .views.Proveedores.views import *
from .views.tipo_servicio.views import *
from .views.compra.views import *
from .views.factura.views import *
from .views.dashboard.views import DashboardView 

app_name = 'app'

urlpatterns = [
    # --- PANEL PRINCIPAL (DASHBOARD) ---
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
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
    #path('acceso/', include(('login.urls', 'login'), namespace='login')),
]