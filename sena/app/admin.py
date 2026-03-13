from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    UsuarioSistema, Empleado,
    Proveedor, Producto, Compra, Cliente,
    Marca, Vehiculo, TipoServicio, OrdenServicio,
    DetalleOrdenProducto, CompatibilidadProducto,
    Factura, Notificacion, Caja,
)


# ══════════════════════════════════════════════════════════
#  USUARIO SISTEMA — registro especial con UserAdmin
#  Sin esto el /admin/ no muestra bien los campos de password
# ══════════════════════════════════════════════════════════
@admin.register(UsuarioSistema)
class UsuarioSistemaAdmin(UserAdmin):
    # Campos extra que aparecen al editar un usuario en /admin/
    fieldsets = UserAdmin.fieldsets + (
        ('Datos del taller', {
            'fields': ('tipo_documento', 'cedula', 'telefono', 'cargo')
        }),
    )
    # Campos extra al crear un usuario nuevo en /admin/
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos del taller', {
            'fields': ('tipo_documento', 'cedula', 'telefono', 'cargo')
        }),
    )
    list_display  = ('username', 'email', 'first_name', 'last_name', 'cargo', 'is_active')
    list_filter   = ('cargo', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cedula')


# ══════════════════════════════════════════════════════════
#  RESTO DE MODELOS
# ══════════════════════════════════════════════════════════
admin.site.register(Empleado)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(Cliente)
admin.site.register(Marca)
admin.site.register(Vehiculo)
admin.site.register(TipoServicio)
admin.site.register(OrdenServicio)
admin.site.register(DetalleOrdenProducto)
admin.site.register(CompatibilidadProducto)
admin.site.register(Factura)
admin.site.register(Notificacion)
admin.site.register(Caja)