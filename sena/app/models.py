from django.db import models
from datetime import datetime
from decimal import Decimal
from app.models import *


# --- MODELOS BASE ---

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=45)
    contrasena = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.nombre}"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "Usuario"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    existencia = models.IntegerField()

    def __str__(self):
        return f" {self.nombre}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "Producto"


class Vehiculo(models.Model):
    tipo_vehiculo = models.CharField(max_length=100)
    placa = models.CharField(max_length=6)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.DateField()
    kilometraje = models.IntegerField()
    documento = models.CharField(max_length=10)

    def _str_(self):
        # Corregido: Retorna una sola cadena.
        return f"{self.marca} {self.modelo}"

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"
        db_table = "Vehiculo"


class insumo(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        # Corregido: Se usa _str_. Retorna una sola cadena.
        return f"{self.nombre} (${self.precio_unitario})"

    class Meta:
        verbose_name = "insumo"
        verbose_name_plural = "insumos"
        db_table = "insumo"


class tipo_servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    duracion_estimada = models.DateField()
    estado = models.BooleanField(default=True)

    def _str_(self):
        return self.nombre

    class Meta:
        verbose_name = "tipo_servicio"
        verbose_name_plural = "tipo_servicios"
        db_table = "tipo_servicio"


class Entrada_vehiculo(models.Model):
    documento = models.IntegerField(unique=True)
    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)
    placa = models.CharField(max_length=6)

    def __str__(self):
        return f"Entrada {self.placa} - {self.fecha_hora_entrada}"

    class Meta:
        db_table = "Entrada_vehiculo"
        verbose_name = "Entrada de Vehículo"
        verbose_name_plural = "Entradas de Vehículos"


# --- MODELOS CON RELACIONES ---

class Proveedores(models.Model):
    nombre = models.CharField(max_length=50)
    documento = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    # Correcto: 'Producto'
    mercancia = models.ForeignKey('Producto', on_delete=models.CASCADE)

    def _str_(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "Proveedor"


class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=10)

    # CORREGIDO: 'Proveedor' -> 'Proveedores' (Nombre de la clase)
    fk_proveedor = models.ForeignKey('Proveedores', on_delete=models.CASCADE)
    # CORREGIDO: 'Insumo' -> 'insumo' (Nombre de la clase)
    fk_insumo = models.ForeignKey('insumo', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"Compra {self.id_compra} - {self.estado}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        db_table = "compra"


class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    # Correcto: 'Producto'
    fk_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    def _str_(self):
        return self.nombre_categoria

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        db_table = "categoria_productos"


class Salida_Vehiculo(models.Model):
    # Correcto: 'Entrada_Vehiculo'
    entrada = models.ForeignKey('Entrada_Vehiculo', on_delete=models.CASCADE)
    fecha_hora_salida = models.DateTimeField()
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f" {self.entrada}"

    class Meta:
        db_table = "salida_vehiculos"
        verbose_name = "Salida de Vehículo"
        verbose_name_plural = "Salidas de Vehículos"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f" {self.nombre}"

    class Meta:
        db_table = "Cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Ventas(models.Model):
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    documento = models.CharField(max_length=10)
    # Correcto: 'Cliente' (Se asumió la creación del modelo Cliente)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    # Correcto: 'Salida_Vehiculo'
    salida = models.ForeignKey('Salida_Vehiculo', on_delete=models.CASCADE)
    # Correcto: 'Producto'
    productos = models.ManyToManyField(Producto)
    # Correcto: 'Usuario'
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def _str_(self):
        # Corregido: Retorna una sola cadena.
        return f"Venta del {self.fecha} a {self.cliente} {self.salida}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "Venta"


class Factura(models.Model):
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # CORREGIDO: 'Venta' -> 'Ventas' (Nombre de la clase)
    venta = models.ForeignKey('Ventas', on_delete=models.CASCADE)

    def _str_(self):
        # Corregido: Retorna una sola cadena.
        return f"Factura #{self.id} por ${self.total}"

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        db_table = "Factura"


class GestionNotificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    mensaje = models.CharField(max_length=45)
    fecha_envio = models.CharField(max_length=45)
    # CORREGIDO: 'Venta' -> 'Ventas' (Nombre de la clase)
    fk_ventas = models.ForeignKey('Ventas', on_delete=models.CASCADE)

    def _str_(self):
        return f"Notificación {self.id_notificacion} - {self.mensaje}"

    class Meta:
        verbose_name = "Gestión de Notificación"
        verbose_name_plural = "Gestión de Notificaciones"
        db_table = "gestion_notificacion"


class Servicio(models.Model):
    descripcion = models.CharField(max_length=255)
    duracion = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    documento = models.IntegerField()

    # Correcto: 'Entrada_Vehiculo'
    entrada = models.ForeignKey('Entrada_Vehiculo', on_delete=models.CASCADE)
    # CORREGIDO: 'Insumos' -> 'insumo' (Nombre de la clase)
    insumo = models.ForeignKey('insumo', on_delete=models.SET_NULL, null=True)
    # Correcto: 'Usuario'
    usuario = models.ForeignKey(
        'Usuario', on_delete=models.SET_NULL, null=True)
    # CORREGIDO: 'TipoServicio' -> 'tipo_servicio' (Nombre de la clase)
    tipo_servicio = models.ForeignKey(
        'tipo_servicio', on_delete=models.CASCADE)

    def _str_(self):
        return f"Servicio {self.descripcion} (${self.precio})"

    class Meta:
        db_table = "servicios"
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
