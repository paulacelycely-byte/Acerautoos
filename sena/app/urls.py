from django.urls import path
from .views.dashboard.views import DashboardView
from .views.Cliente.views import (ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView)
from .views.Vehiculo.views import (VehiculoListView, VehiculoCreateView, VehiculoUpdateView, VehiculoDeleteView)
from .views.Usuario.views import (UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView)
#from .views.compra.views import (CompraListView, CompraCreateView, CompraUpdateView, CompraDeleteView)
from .views.Proveedor.views import (ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView)
from .views.Marca.views import (MarcaListView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView)
from .views.Producto.views import (ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView)

app_name = 'app'

urlpatterns = [

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # --- CLIENTES ---
    path('clientes/listar/', ClienteListView.as_view(), name='listar_clientes'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('clientes/editar/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),

    # --- VEHICULOS ---
    path('vehiculos/listar/', VehiculoListView.as_view(), name='listar_vehiculos'),
    path('vehiculos/crear/', VehiculoCreateView.as_view(), name='crear_vehiculo'),
    path('vehiculos/editar/<int:pk>/', VehiculoUpdateView.as_view(), name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/', VehiculoDeleteView.as_view(), name='eliminar_vehiculo'),

    # --- COMPRAS ---
    #path('compras/listar/', CompraListView.as_view(), name='lista_compras'),
    #path('compras/crear/', CompraCreateView.as_view(), name='crear_compra'),
    #path('compras/editar/<int:pk>/', CompraUpdateView.as_view(), name='editar_compra'),

    # --- PROVEEDORES ---
    path('proveedor/listar/', ProveedorListView.as_view(), name='listar_proveedores'),
    path('proveedor/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),

    # --- MARCAS ---
    path('marca/listar/', MarcaListView.as_view(), name='listar_marca'),
    path('marca/crear/', MarcaCreateView.as_view(), name='crear_marca'),
    path('marca/editar/<int:pk>/', MarcaUpdateView.as_view(), name='editar_marca'),
    path('marca/eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='eliminar_marca'),

    # --- USUARIOS ---
    path('usuarios/listar/', UsuarioListView.as_view(), name='listar_usuario'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),

    # --- PRODUCTOS ---
    path('producto/listar/', ProductoListView.as_view(), name='listar_producto'),
    path('producto/crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),

]