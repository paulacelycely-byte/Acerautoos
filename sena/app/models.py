from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# --- USUARIO ---
class Usuario(models.Model):
    CARGOS = [('ADMIN', 'Administrador'), ('MECANICO', 'Mecánico'), ('RECEPCIONISTA', 'Recepcionista'), ('GERENTE', 'Gerente')]
    TIPOS_DOC = [('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('NIT', 'NIT'), ('PAS', 'Pasaporte')]
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DOC, default='CC')
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    password_confirmacion = models.CharField(max_length=128, null=True, blank=True)
    cargo = models.CharField(max_length=20, choices=CARGOS, default='ADMIN')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        db_table = 'usuario'

# --- MARCA ---
class Marca(models.Model):
    CATEGORIAS = [('AUTO', 'Marca de Vehículo'), ('REPUESTO', 'Marca de Repuesto/Aceite')]
    nombre = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default='AUTO')
    pais_origen = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='marcas_logos/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

# --- CAJA ---
class Caja(models.Model):
    TIPOS = [('INGRESO', 'Ingreso (+)'), ('EGRESO', 'Egreso (-)')]
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPOS)

    class Meta:
        db_table = "caja"

# --- PROVEEDOR ---
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.nombre

# --- PRODUCTO ---
class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, limit_choices_to={'categoria': 'REPUESTO'})
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    codigo = models.CharField(max_length=20, unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} | Stock: {self.stock}"

# --- COMPATIBILIDAD ---
class CompatibilidadProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    marca_vehiculo = models.ForeignKey(Marca, on_delete=models.CASCADE, limit_choices_to={'categoria': 'AUTO'})
    
    def __str__(self):
        return f"{self.producto.nombre} aplica para {self.marca_vehiculo.nombre}"

# --- COMPRA ---
class Compra(models.Model):
    METODOS = [('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia'), ('Credito', 'Crédito')]
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    num_factura_proveedor = models.CharField(max_length=50, unique=True) 
    metodo_pago = models.CharField(max_length=20, choices=METODOS, default='Efectivo')
    total_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.producto.stock += self.cantidad
            self.producto.save()
            if self.metodo_pago != 'Credito':
                Caja.objects.create(descripcion=f"Compra Factura {self.num_factura_proveedor}", monto=self.total_pagado, tipo='EGRESO')
        super().save(*args, **kwargs)

# --- CLIENTE, VEHICULO, SERVICIO, ORDEN ---
class Cliente(models.Model):
    TIPOS_DOC = [('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('NIT', 'NIT'), ('PAS', 'Pasaporte')]
    nombre = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DOC, default='CC')
    numero_documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, limit_choices_to={'categoria': 'AUTO'})
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio_mano_obra = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.nombre

class OrdenServicio(models.Model):
    ESTADOS = [('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Terminado', 'Terminado')]
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    servicio = models.ForeignKey(TipoServicio, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    km_actual = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    def __str__(self):
        return f"Orden {self.id}"

# --- DETALLE ---
class DetalleOrdenProducto(models.Model):
    orden = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name='productos_usados')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk: 
            if self.producto.stock < self.cantidad:
                raise ValidationError(f"¡No hay suficiente stock de {self.producto.nombre}!")
            self.producto.stock -= self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.producto.stock += self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)

# --- VENTAS ---
class VentasFactura(models.Model):
    orden = models.OneToOneField(OrdenServicio, on_delete=models.CASCADE, related_name='factura')
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            Caja.objects.create(descripcion=f"Venta Factura {self.numero_factura}", monto=self.total, tipo='INGRESO')
            self.orden.estado = 'Terminado'
            self.orden.save()
        super().save(*args, **kwargs)

# --- NOTIFICACIÓN ---
class Notificacion(models.Model):
    tipo = models.CharField(max_length=50)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)