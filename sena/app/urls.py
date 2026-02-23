from django.urls import path
from app.views.categorias.views import *
from app.views.Salida_vehiculo.views import *
from app.views.Insumos.views import *
from app.views.Servicio.views import *

app_name = 'app'

urlpatterns = [

    # ===== CATEGORÍAS =====
    path('listar_categorias/', categoriaListView.as_view(), name='listar_categoria'),
    path('crear_categoria/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    
    
     # ===== SALIDA VEHÍCULO =====
    path('listar_salida_vehiculo/', Salida_vehiculoListView.as_view(), name='listar_salida_vehiculo'),
    path('crear_salida_vehiculo/', Salida_vehiculoCreateView.as_view(), name='crear_salida_vehiculo'),
    path('editar_salida_vehiculo/<int:pk>/', Salida_vehiculoUpdateView.as_view(), name='editar_salida_vehiculo'),
    path('eliminar_salida_vehiculo/<int:pk>/', Salida_vehiculoDeleteView.as_view(), name='eliminar_salida_vehiculo'),
    
    
     # ===== INSUMOS =====
    path('listar_insumo/', InsumoListView.as_view(), name='listar_insumo'),
    path('crear_insumo/', InsumoCreateView.as_view(), name='crear_insumo'),
    path('editar_insumo/<int:pk>/', InsumoUpdateView.as_view(), name='editar_insumo'),
    path('eliminar_insumo/<int:pk>/', InsumoDeleteView.as_view(), name='eliminar_insumo'),
    
        # ===== SERVICIO =====  
    path('listar_servicio/', ServicioListView.as_view(), name='listar_servicio'),
    path('crear_servicio/', ServicioCreateView.as_view(), name='crear_servicio'),           
    path('editar_servicio/<int:pk>/', ServicioUpdateView.as_view(), name='editar_servicio'),
    path('eliminar_servicio/<int:pk>/', ServicioDeleteView.as_view(), name='eliminar_servicio'),
    
    
]

