from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# =========================================================
# BLOQUE 0: PERSONAL (USUARIOS)
# =========================================================
class Usuario(models.Model):
    CARGOS = [
        ('ADMIN', 'Administrador'),
        ('MECANICO', 'Mecánico'),
        ('RECEPCIONISTA', 'Recepcionista'),
        ('GERENTE', 'Gerente'),
    ]
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    cargo = models.CharField(max_length=20, choices=CARGOS, default='ADMIN')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.get_cargo_display()})"

    class Meta:
        db_table = 'usuario'
        ordering = ['id']


# =========================================================
# BLOQUE 1: INVENTARIO Y FINANZAS (CAJA)
# =========================================================
class Marca(models.Model):

    nombre = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
                message='El nombre solo puede contener letras y espacios.'
            )
        ]
    )

    pais_origen = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    estado = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre

class Caja(models.Model):
    TIPOS = [('INGRESO', 'Ingreso (+)'), ('EGRESO', 'Egreso (-)')]
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPOS)

    def __str__(self):
        return f"{self.tipo}: {self.descripcion} (${self.monto})"

    class Meta:
        db_table = "caja"
        verbose_name_plural = "Cajas"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "proveedor"


class Producto(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$',
                message='El nombre solo puede contener letras, números y espacios.'
            )
        ]
    )

    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        limit_choices_to={'estado': True}  # Solo marcas activas
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    stock_minimo = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    codigo = models.CharField(
        max_length=20,
        unique=True
    )

    estado = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def clean(self):
        # Validación lógica empresarial
        if self.stock_minimo > self.stock:
            raise ValidationError(
                "El stock mínimo no puede ser mayor al stock actual."
            )

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

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
                Caja.objects.create(
                    descripcion=f"Pago Compra Factura {self.num_factura_proveedor} - {self.proveedor.nombre}",
                    monto=self.total_pagado,
                    tipo='EGRESO'
                )
        super().save(*args, **kwargs)

    class Meta:
        db_table = "compra"


# =========================================================
# BLOQUE 2: CLIENTES Y FLOTA
# =========================================================
class Cliente(models.Model):
    TIPOS_DOC = [('CC', 'Cédula'), ('NIT', 'NIT'), ('CE', 'Cédula Extranjería')]
    nombre = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=5, choices=TIPOS_DOC, default='CC')
    numero_documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.numero_documento}"

    class Meta:
        db_table = "cliente"

# 🔥 MARCA MEJORADA PROFESIONALMENTE
from django.db import models
from django.core.validators import RegexValidator



class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    Marca = models.ForeignKey('Marca', on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} ({self.marca} {self.modelo})"

    class Meta:
        db_table = "vehiculo"


# =========================================================
# BLOQUE 3: OPERACIÓN
# =========================================================
class TipoServicio(models.Model):
    Tipo = [
    ('CB','Cambio de aceite'),
    ('CF', 'Cambio de filtros'),
    ('FR', 'Revisión de frenos'),
    ('AF', 'Cambio de amortiguadores'),
    ('CL', 'Cambio de llantas'),
    ('TB', 'Cambio de batería'),
    ('LB', 'Lavado básico'),
    ('CM', 'Cambio de motor'),
    ('CT', 'Cambio de transmisión'),
    ('RI', 'Revisión de inyección'),
    ('CE', 'Cambio de embrague'),
    
]
    
    nombre = models.CharField(max_length=100,choices=Tipo)
    precio_mano_obra = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "tipo_servicio"


class OrdenServicio(models.Model):  # 🔥 CORREGIDO
    ESTADOS = [('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Terminado', 'Terminado')]
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    servicio = models.ForeignKey(TipoServicio, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    km_actual = models.IntegerField()
    km_proximo_cambio = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Orden {self.id} - {self.vehiculo.placa}"

    class Meta:
        db_table = "orden_servicio"



class DetalleOrdenProducto(models.Model):
    orden = models.ForeignKey(
        'OrdenServicio',
        on_delete=models.CASCADE,
        related_name='productos_usados'
    )
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(default=1)

    def clean(self):
        # Validar cantidad mayor a 0
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")

    def __str__(self):
        return f"{self.producto.nombre} - Cantidad: {self.cantidad}"
    
    class Meta:
        db_table = 'DetalleProducto'
        

# =========================================================
# BLOQUE 4: FACTURACIÓN Y ALERTAS
# =========================================================
class VentasFactura(models.Model):
    METODOS = [('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia')]

    venta = models.OneToOneField(
        'OrdenServicio',
        on_delete=models.CASCADE
    )

    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20, choices=METODOS, default='Efectivo')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            Caja.objects.create(
                descripcion=f"Venta Factura {self.numero_factura} - Orden {self.orden.id}",
                monto=self.total,
                tipo='INGRESO'
            )
        super().save(*args, **kwargs)

    class Meta:
        db_table = "factura"


class Notificacion(models.Model):
    TIPOS = [('Mantenimiento', 'Mantenimiento'), ('Stock', 'Inventario Bajo')]
    tipo = models.CharField(max_length=20, choices=TIPOS, default='Mantenimiento')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        db_table = "notificacion"