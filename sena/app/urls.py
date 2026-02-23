from django.urls import path
from .views.categorias.views import *
from .views.Proveedores.views import *
from .views.tipo_servicio.views import *  

app_name = 'app'

urlpatterns = [
    # --- MÓDULO DE CATEGORÍAS ---
    path('listar_categorias/', categoriaListView.as_view(), name='listar_categoria'),
    path('crear_categoria/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    
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
]