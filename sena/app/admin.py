from django.contrib import admin
from .models import (
    Proveedor, Producto, Compra, Cliente, 
    Marca, Vehiculo, TipoServicio, OrdenServicio, VentasFactura
)


admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(Cliente)
admin.site.register(Marca)
admin.site.register(Vehiculo)
admin.site.register(TipoServicio)
admin.site.register(OrdenServicio)
admin.site.register(VentasFactura)