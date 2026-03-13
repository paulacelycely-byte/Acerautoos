from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


# ══════════════════════════════════════════════════════════
#  USUARIO SISTEMA  
# ══════════════════════════════════════════════════════════
class UsuarioSistema(AbstractUser):
    CARGOS = [
        ('ADMIN',         'Administrador'),
        ('MECANICO',      'Mecánico'),
        ('RECEPCIONISTA', 'Recepcionista'),
        ('GERENTE',       'Gerente'),
    ]
    TIPOS_DOC = [
        ('CC',  'Cédula de Ciudadanía'),
        ('CE',  'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
    ]

    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DOC, default='CC')
    cedula         = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono       = models.CharField(max_length=20, null=True, blank=True)
    cargo          = models.CharField(max_length=20, choices=CARGOS, default='ADMIN')

    # auth.User ya trae: username, first_name, last_name, email,
    #                    password, is_active, last_login, date_joined

    @property
    def nombre_completo(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def inicial(self):
        return (self.first_name[0] if self.first_name else self.username[0]).upper()

    def __str__(self):
        return self.nombre_completo

    class Meta:
        db_table     = 'usuario_sistema'
        verbose_name = 'Usuario del Sistema'


# ══════════════════════════════════════════════════════════
#  EMPLEADO  (directorio del personal)
# ══════════════════════════════════════════════════════════
class Empleado(models.Model):
    CARGOS = [
        ('ADMIN',         'Administrador'),
        ('MECANICO',      'Mecánico'),
        ('RECEPCIONISTA', 'Recepcionista'),
        ('GERENTE',       'Gerente'),
    ]
    TIPOS_DOC = [
        ('CC',  'Cédula de Ciudadanía'),
        ('CE',  'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
    ]

    nombres        = models.CharField(max_length=150)
    apellidos      = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DOC, default='CC')
    cedula         = models.CharField(max_length=20, unique=True)
    telefono       = models.CharField(max_length=20, null=True, blank=True)
    correo         = models.EmailField(unique=True)
    cargo          = models.CharField(max_length=20, choices=CARGOS, default='MECANICO')
    activo         = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now=True)

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def inicial(self):
        return self.nombres[0].upper() if self.nombres else "E"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} — {self.get_cargo_display()}"

    class Meta:
        db_table     = 'empleado'
        verbose_name = 'Empleado'


# ══════════════════════════════════════════════════════════
#  MARCA
# ══════════════════════════════════════════════════════════
class Marca(models.Model):
    CATEGORIAS = [
        ('AUTO',     'Marca de Vehículo'),
        ('REPUESTO', 'Marca de Repuesto/Aceite'),
    ]
    nombre         = models.CharField(max_length=50, unique=True)
    categoria      = models.CharField(max_length=10, choices=CATEGORIAS, default='AUTO')
    pais_origen    = models.CharField(max_length=50, blank=True, null=True)
    logo           = models.ImageField(upload_to='marcas_logos/', blank=True, null=True)
    descripcion    = models.TextField(blank=True, null=True)
    estado         = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

    class Meta:
        db_table = 'marca'


# ══════════════════════════════════════════════════════════
#  CAJA
# ══════════════════════════════════════════════════════════
class Caja(models.Model):
    TIPOS = [('INGRESO', 'Ingreso (+)'), ('EGRESO', 'Egreso (-)')]
    CATEGORIAS = [
        ('Ventas',            'Ventas'),
        ('Servicios',         'Servicios'),
        ('Anticipos',         'Anticipos de clientes'),
        ('Arriendo',          'Arriendo'),
        ('ServiciosPublicos', 'Servicios públicos'),
        ('Proveedores',       'Pago a proveedores'),
        ('Nomina',            'Nómina / Salarios'),
        ('Mantenimiento',     'Mantenimiento'),
        ('Otros',             'Otros'),
    ]
    METODOS_PAGO = [
        ('Efectivo',       'Efectivo'),
        ('Transferencia',  'Transferencia bancaria'),
        ('TarjetaDebito',  'Tarjeta débito'),
        ('TarjetaCredito', 'Tarjeta crédito'),
        ('Cheque',         'Cheque'),
        ('Nequi',          'Nequi'),
        ('Daviplata',      'Daviplata'),
    ]
    descripcion   = models.CharField(max_length=255)
    monto         = models.DecimalField(max_digits=12, decimal_places=2)
    tipo          = models.CharField(max_length=10, choices=TIPOS)
    fecha         = models.DateTimeField(default=timezone.now)
    categoria     = models.CharField(max_length=20, choices=CATEGORIAS, default='Otros')
    metodo_pago   = models.CharField(max_length=20, choices=METODOS_PAGO, default='Efectivo')
    comprobante   = models.FileField(upload_to='caja_comprobantes/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} | {self.descripcion} | ${self.monto}"

    class Meta:
        db_table = 'caja'


# ══════════════════════════════════════════════════════════
#  PROVEEDOR
# ══════════════════════════════════════════════════════════
class Proveedor(models.Model):
    nombre    = models.CharField(max_length=100)
    nit       = models.CharField(max_length=20, unique=True)
    telefono  = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'proveedor'


# ══════════════════════════════════════════════════════════
#  PRODUCTO
# ══════════════════════════════════════════════════════════
class Producto(models.Model):
    nombre       = models.CharField(max_length=100, unique=True)
    marca        = models.ForeignKey(
        Marca, on_delete=models.PROTECT,
        # FIX: solo marcas activas de tipo REPUESTO
        limit_choices_to={'categoria': 'REPUESTO', 'estado': True}
    )
    proveedor    = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    descripcion  = models.TextField(blank=True, null=True)
    precio       = models.DecimalField(max_digits=10, decimal_places=2)
    stock        = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    codigo       = models.CharField(max_length=20, unique=True)
    estado       = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} | Stock: {self.stock}"

    class Meta:
        db_table = 'producto'


# ══════════════════════════════════════════════════════════
#  TIPO SERVICIO
# ══════════════════════════════════════════════════════════
class TipoServicio(models.Model):
    nombre           = models.CharField(max_length=100)
    precio_mano_obra = models.DecimalField(max_digits=12, decimal_places=2)
    intervalo_km     = models.PositiveIntegerField(
        default=0,
        help_text="Cada cuántos km se repite este servicio. Ej: 5000 para cambio de aceite. 0 = no aplica."
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipo_servicio'


# ══════════════════════════════════════════════════════════
#  COMPATIBILIDAD PRODUCTO
# ══════════════════════════════════════════════════════════
class CompatibilidadProducto(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE,
        # FIX: solo productos activos
        limit_choices_to={'estado': True}
    )
    marca_vehiculo = models.ForeignKey(
        Marca, on_delete=models.CASCADE,
        # FIX: solo marcas activas de tipo AUTO
        limit_choices_to={'categoria': 'AUTO', 'estado': True}
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio, on_delete=models.CASCADE,
        null=True, blank=True,
        help_text="Servicio donde se usa este producto. Dejar vacío si aplica para cualquiera."
    )

    def __str__(self):
        srv = f" — {self.tipo_servicio.nombre}" if self.tipo_servicio else ""
        return f"{self.producto.nombre} → {self.marca_vehiculo.nombre}{srv}"

    class Meta:
        db_table        = 'compatibilidad_producto'
        unique_together = ('producto', 'marca_vehiculo', 'tipo_servicio')


# ══════════════════════════════════════════════════════════
#  CLIENTE
# ══════════════════════════════════════════════════════════
class Cliente(models.Model):
    TIPOS_DOC = [
        ('CC',  'Cédula de Ciudadanía'),
        ('CE',  'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
    ]
    nombre           = models.CharField(max_length=150)
    tipo_documento   = models.CharField(max_length=3, choices=TIPOS_DOC, default='CC')
    numero_documento = models.CharField(max_length=20, unique=True)
    telefono         = models.CharField(max_length=20)
    email            = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'cliente'


# ══════════════════════════════════════════════════════════
#  VEHICULO
# ══════════════════════════════════════════════════════════
class Vehiculo(models.Model):
    placa   = models.CharField(max_length=10, unique=True)
    modelo  = models.CharField(max_length=50, help_text="Año del vehículo. Ej: 2019")
    marca   = models.ForeignKey(
        Marca, on_delete=models.PROTECT,
        # FIX: solo marcas activas de tipo AUTO
        limit_choices_to={'categoria': 'AUTO', 'estado': True}
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    km_ultimo_servicio       = models.IntegerField(
        default=0,
        help_text="Se actualiza automáticamente al registrar una orden de servicio."
    )
    km_proximo_mantenimiento = models.IntegerField(
        null=True, blank=True,
        help_text="Se calcula automáticamente. Puede sobreescribirse manualmente."
    )

    def __str__(self):
        return f"{self.placa} - {self.modelo} ({self.marca.nombre})"

    class Meta:
        db_table = 'vehiculo'


# ══════════════════════════════════════════════════════════
#  ORDEN DE SERVICIO
# ══════════════════════════════════════════════════════════
class OrdenServicio(models.Model):
    ESTADOS = [
        ('Pendiente',  'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Terminado',  'Terminado'),
    ]
    # FIX: usa Empleado en lugar del antiguo Usuario
    empleado = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'activo': True}
    )
    vehiculo  = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    servicio  = models.ForeignKey(TipoServicio, on_delete=models.PROTECT)
    fecha     = models.DateTimeField(default=timezone.now)
    km_actual = models.IntegerField()
    estado    = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._actualizar_km_vehiculo()

    def _actualizar_km_vehiculo(self):
        """
        Actualiza km del vehículo y genera notificación
        de mantenimiento si está cerca del próximo servicio.
        """
        vehiculo = self.vehiculo
        servicio = self.servicio

        if self.km_actual > vehiculo.km_ultimo_servicio:
            vehiculo.km_ultimo_servicio = self.km_actual

            if servicio.intervalo_km > 0:
                nuevo_proximo = self.km_actual + servicio.intervalo_km
                if (
                    vehiculo.km_proximo_mantenimiento is None or
                    nuevo_proximo < vehiculo.km_proximo_mantenimiento
                ):
                    vehiculo.km_proximo_mantenimiento = nuevo_proximo

            vehiculo.save(update_fields=['km_ultimo_servicio', 'km_proximo_mantenimiento'])

            # Notificación si faltan 1000 km o menos para el próximo mantenimiento
            if vehiculo.km_proximo_mantenimiento:
                km_restante = vehiculo.km_proximo_mantenimiento - self.km_actual
                if km_restante <= 1000:
                    Notificacion.objects.get_or_create(
                        tipo     = 'Mantenimiento',
                        origen   = 'SISTEMA',
                        leido    = False,
                        vehiculo = vehiculo,
                        defaults = {
                            'titulo': f"Mantenimiento próximo — {vehiculo.placa}",
                            'mensaje': (
                                f"El vehículo {vehiculo.placa} ({vehiculo.marca.nombre} {vehiculo.modelo}) "
                                f"tiene {self.km_actual} km actuales. "
                                f"Próximo mantenimiento a los {vehiculo.km_proximo_mantenimiento} km "
                                f"(faltan aprox. {max(km_restante, 0)} km)."
                            ),
                        }
                    )

    def __str__(self):
        return f"Orden #{self.id} — {self.vehiculo.placa}"

    class Meta:
        db_table = 'orden_servicio'


# ══════════════════════════════════════════════════════════
#  COMPRA
# ══════════════════════════════════════════════════════════
class Compra(models.Model):
    METODOS = [
        ('Efectivo',      'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Credito',       'Crédito'),
    ]
    proveedor             = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto              = models.ForeignKey(
        Producto, on_delete=models.CASCADE,
        # FIX: solo productos activos
        limit_choices_to={'estado': True}
    )
    cantidad              = models.IntegerField()
    fecha                 = models.DateTimeField(default=timezone.now)
    num_factura_proveedor = models.CharField(max_length=50, unique=True)
    metodo_pago           = models.CharField(max_length=20, choices=METODOS, default='Efectivo')
    total_pagado          = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.producto.stock += self.cantidad
            self.producto.save()

            if self.metodo_pago != 'Credito':
                Caja.objects.create(
                    descripcion = f"Compra Factura {self.num_factura_proveedor}",
                    monto       = self.total_pagado,
                    tipo        = 'EGRESO',
                    categoria   = 'Proveedores',
                    metodo_pago = self.metodo_pago,
                )

            # Notificación si sigue bajo el mínimo incluso tras la compra
            prod = Producto.objects.get(pk=self.producto.pk)
            if prod.stock <= prod.stock_minimo:
                Notificacion.objects.get_or_create(
                    tipo   = 'Alerta',
                    origen = 'SISTEMA',
                    leido  = False,
                    titulo = f"Stock bajo — {prod.nombre}",
                    defaults={
                        'mensaje': (
                            f"'{prod.nombre}' tiene {prod.stock} unidades, "
                            f"igual o por debajo del mínimo ({prod.stock_minimo})."
                        ),
                    }
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra #{self.id} — {self.producto.nombre}"

    class Meta:
        db_table = 'compra'


# ══════════════════════════════════════════════════════════
#  DETALLE ORDEN
# ══════════════════════════════════════════════════════════
class DetalleOrdenProducto(models.Model):
    orden    = models.ForeignKey(
        OrdenServicio, on_delete=models.CASCADE,
        related_name='productos_usados'
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT,
        # FIX: solo productos activos
        limit_choices_to={'estado': True}
    )
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.producto.stock < self.cantidad:
                raise ValidationError(
                    f"Stock insuficiente para '{self.producto.nombre}'. "
                    f"Disponible: {self.producto.stock}."
                )
            self.producto.stock -= self.cantidad
            self.producto.save()

            # Notificación si baja del mínimo
            prod = Producto.objects.get(pk=self.producto.pk)
            if prod.stock <= prod.stock_minimo:
                Notificacion.objects.get_or_create(
                    tipo   = 'Alerta',
                    origen = 'SISTEMA',
                    leido  = False,
                    titulo = f"Stock bajo — {prod.nombre}",
                    defaults={
                        'mensaje': (
                            f"'{prod.nombre}' bajó a {prod.stock} unidades "
                            f"tras usarse en la Orden #{self.orden.id}. "
                            f"Mínimo permitido: {prod.stock_minimo}."
                        ),
                    }
                )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.producto.stock += self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} — Orden #{self.orden.id}"

    class Meta:
        db_table = 'detalle_orden_producto'


# ══════════════════════════════════════════════════════════
#  FACTURA  (modelo unificado — reemplaza VentasFactura)
# ══════════════════════════════════════════════════════════
class Factura(models.Model):
    TIPO_FACTURA = [
        ('SERVICIO', 'Orden de Servicio'),
        ('PRODUCTO', 'Venta de Producto'),
    ]
    METODOS_PAGO = [
        ('Efectivo',       'Efectivo'),
        ('Transferencia',  'Transferencia Bancaria'),
        ('TarjetaDebito',  'Tarjeta Débito'),
        ('TarjetaCredito', 'Tarjeta Crédito'),
        ('Nequi',          'Nequi'),
        ('Daviplata',      'Daviplata'),
    ]
    ESTADOS_PAGO = [
        ('Pendiente', 'Pendiente'),
        ('Pagada',    'Pagada'),
    ]

    tipo           = models.CharField(max_length=10, choices=TIPO_FACTURA, default='SERVICIO')
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision  = models.DateTimeField(auto_now_add=True)

    orden_servicio = models.ForeignKey(
        'OrdenServicio', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='facturas'
    )
    producto = models.ForeignKey(
        'Producto', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='facturas',
        # FIX: solo productos activos
        limit_choices_to={'estado': True}
    )
    cantidad  = models.PositiveIntegerField(default=1, null=True, blank=True)
    subtotal  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva       = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total     = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    estado_pago = models.CharField(max_length=10, choices=ESTADOS_PAGO, default='Pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, null=True, blank=True)
    fecha_pago  = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.tipo == 'SERVICIO' and not self.orden_servicio:
            raise ValidationError("Debe seleccionar una Orden de Servicio.")
        if self.tipo == 'PRODUCTO' and not self.producto:
            raise ValidationError("Debe seleccionar un Producto.")

    def save(self, *args, **kwargs):
        if self.estado_pago == 'Pagada' and not self.fecha_pago:
            self.fecha_pago = timezone.now()

        super().save(*args, **kwargs)

        if self.estado_pago == 'Pagada':
            if not Caja.objects.filter(descripcion__icontains=self.numero_factura).exists():
                Caja.objects.create(
                    descripcion = f"Factura {self.numero_factura} — {self.get_tipo_display()}",
                    monto       = self.total,
                    tipo        = 'INGRESO',
                    categoria   = 'Ventas' if self.tipo == 'PRODUCTO' else 'Servicios',
                    metodo_pago = self.metodo_pago or 'Efectivo',
                )
                if self.tipo == 'SERVICIO' and self.orden_servicio:
                    self.orden_servicio.estado = 'Terminado'
                    self.orden_servicio.save()

    def __str__(self):
        return f"Factura {self.numero_factura} — {self.get_tipo_display()}"

    class Meta:
        db_table = 'factura'
        ordering = ['-fecha_emision']


# ══════════════════════════════════════════════════════════
#  NOTIFICACION
# ══════════════════════════════════════════════════════════
class Notificacion(models.Model):
    TIPOS = [
        ('Alerta',        'Alerta'),
        ('Recordatorio',  'Recordatorio'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Urgente',       'Urgente'),
        ('Informacion',   'Información'),
    ]
    ORIGENES = [
        ('SISTEMA', 'Automática del sistema'),
        ('ADMIN',   'Creada por administrador'),
    ]

    tipo     = models.CharField(max_length=50, choices=TIPOS)
    origen   = models.CharField(max_length=10, choices=ORIGENES, default='ADMIN')
    titulo   = models.CharField(max_length=150, blank=True)
    # FIX: vehiculo opcional — notif. de stock no tienen vehículo
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE,
        null=True, blank=True,
        help_text="Solo si la notificación está relacionada con un vehículo."
    )
    mensaje  = models.TextField()
    leido    = models.BooleanField(default=False)
    fecha    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_origen_display()}] {self.tipo} — {self.titulo or self.mensaje[:40]}"

    class Meta:
        db_table = 'notificacion'
        ordering = ['-fecha']