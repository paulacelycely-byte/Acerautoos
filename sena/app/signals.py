"""from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import DetalleOrdenProducto, Producto

# ==============================================
# DESCARGAR STOCK AL CREAR O MODIFICAR DETALLE
# ==============================================
@receiver(post_save, sender=DetalleOrdenProducto)
def actualizar_stock_producto(sender, instance, created, **kwargs):
    producto = instance.producto

    if created:
        # 🔹 Nuevo detalle → descontar stock
        if producto.existencia < instance.cantidad:
            raise ValidationError(
                f"No hay suficiente stock de {producto.nombre}. Disponible: {producto.existencia}"
            )
        producto.existencia -= instance.cantidad
        producto.save()
    else:
        # 🔹 Se editó la cantidad → ajustar diferencia
        detalle_anterior = DetalleOrdenProducto.objects.get(pk=instance.pk)
        diferencia = instance.cantidad - detalle_anterior.cantidad
        if diferencia > 0 and producto.existencia < diferencia:
            raise ValidationError(
                f"No hay suficiente stock para aumentar la cantidad de {producto.nombre}. Disponible: {producto.existencia}"
            )
        producto.existencia -= diferencia
        producto.save()


# ==============================================
# DEVOLVER STOCK AL ELIMINAR DETALLE
# ==============================================
@receiver(post_delete, sender=DetalleOrdenProducto)
def devolver_stock_producto(sender, instance, **kwargs):
    producto = instance.producto
    producto.existencia += instance.cantidad
    producto.save()"""