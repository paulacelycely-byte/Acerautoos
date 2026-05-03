from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# ══════════════════════════════════════════════════════════
#  USUARIO SISTEMA
# ══════════════════════════════════════════════════════════
class UsuarioSistema(AbstractUser):
    CARGOS = [
        ('ADMIN',         'Administrador'),
        ('MECANICO',      'Mecánico'),

    ]
    TIPOS_DOC = [
        ('CC',  'Cédula de Ciudadanía'),
        ('CE',  'Cédula de Extranjería'),
        ('PAS', 'Pasaporte'),
    ]
    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DOC, default='CC')
    cedula         = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono       = models.CharField(max_length=20, null=True, blank=True)
    cargo          = models.CharField(max_length=20, choices=CARGOS, default='ADMIN')

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
#  EMPLEADO
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
    nombre         = models.CharField(max_length=50)
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
        ('Ventas', 'Ventas'),
        ('Servicios', 'Servicios'),
        ('Anticipos', 'Anticipos de clientes'),
        ('Arriendo', 'Arriendo'),
        ('ServiciosPublicos', 'Servicios públicos'),
        ('Proveedores', 'Pago a proveedores'),
        ('Nomina', 'Nómina / Salarios'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Otros', 'Otros'),
    ]
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia bancaria'),
        ('TarjetaDebito', 'Tarjeta débito'),
        ('TarjetaCredito', 'Tarjeta crédito'),
        ('Cheque', 'Cheque'),
        ('Nequi', 'Nequi'),
        ('Daviplata', 'Daviplata'),
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
    activo    = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'proveedor'


# ══════════════════════════════════════════════════════════
#  PRODUCTO
# ══════════════════════════════════════════════════════════
class Producto(models.Model):
    UNIDADES = [
        ('UND', 'Unidad'), ('LT', 'Litro'), ('ML', 'Mililitro'),
        ('KG', 'Kilogramo'), ('GR', 'Gramo'), ('MT', 'Metro'),
        ('CM', 'Centímetro'), ('GL', 'Galón'), ('PAR', 'Par'),
        ('KIT', 'Kit'), ('CJA', 'Caja'), ('RLL', 'Rollo'), ('JGO', 'Juego'),
    ]
    nombre        = models.CharField(max_length=100, unique=True)
    marca         = models.ForeignKey(Marca, on_delete=models.PROTECT, limit_choices_to={'categoria': 'REPUESTO', 'estado': True})
    proveedor     = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion   = models.TextField(blank=True, null=True)
    precio        = models.DecimalField(max_digits=10, decimal_places=2)
    stock         = models.PositiveIntegerField(default=0)
    stock_minimo  = models.PositiveIntegerField(default=0)
    codigo        = models.CharField(max_length=20, unique=True)
    unidad_medida = models.CharField(max_length=5, choices=UNIDADES, default='UND', verbose_name='Unidad de medida')
    imagen        = models.ImageField(upload_to='productos/', blank=True, null=True)
    estado        = models.BooleanField(default=True)

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
    intervalo_km     = models.PositiveIntegerField(default=0, help_text="Ej: 5000 para aceite.")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipo_servicio'


# ══════════════════════════════════════════════════════════
#  COMPATIBILIDAD PRODUCTO
# ══════════════════════════════════════════════════════════
class CompatibilidadProducto(models.Model):
    producto       = models.ForeignKey(Producto, on_delete=models.CASCADE, limit_choices_to={'estado': True})
    marca_vehiculo = models.ForeignKey(Marca, on_delete=models.CASCADE, limit_choices_to={'categoria': 'AUTO', 'estado': True})
    tipo_servicio  = models.ForeignKey(TipoServicio, on_delete=models.CASCADE, null=True, blank=True)

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
    TIPOS_DOC = [('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('PAS', 'Pasaporte')]
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
    TIPOS_USO = [
        ('BAJO',   'Uso bajo (ciudad, poco uso)'),
        ('NORMAL', 'Uso normal'),
        ('ALTO',   'Uso alto (viajes frecuentes)'),
        ('CARGA',  'Carga / Transporte'),
    ]

    placa   = models.CharField(max_length=10, unique=True)
    modelo  = models.CharField(max_length=50)
    marca   = models.ForeignKey(Marca, on_delete=models.PROTECT, limit_choices_to={'categoria': 'AUTO', 'estado': True})
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    # ── Kilometraje ──
    km_ultimo_servicio       = models.IntegerField(default=0)
    km_proximo_mantenimiento = models.IntegerField(null=True, blank=True)
    km_intervalo             = models.PositiveIntegerField(default=5000, help_text="Cada cuántos km hacer mantenimiento. Ej: 5000")

    # ── Fechas ──
    fecha_ultimo_servicio       = models.DateField(null=True, blank=True)
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True)
    intervalo_meses             = models.PositiveIntegerField(default=3, help_text="Cada cuántos meses hacer mantenimiento. Ej: 3")

    # ── Tipo de uso (reemplaza km_diarios_promedio) ──
    tipo_uso = models.CharField(max_length=10, choices=TIPOS_USO, default='NORMAL')

    # ── Alerta ──
    km_alerta_anticipacion = models.PositiveIntegerField(default=500, help_text="Con cuántos km de anticipación avisar")

    def km_diarios(self):
        """Retorna km diarios estimados según tipo de uso."""
        return {'BAJO': 30, 'NORMAL': 50, 'ALTO': 80, 'CARGA': 120}.get(self.tipo_uso, 50)

    def km_estimados_hoy(self):
        if not self.fecha_ultimo_servicio:
            return self.km_ultimo_servicio
        dias = (timezone.now().date() - self.fecha_ultimo_servicio).days
        return self.km_ultimo_servicio + (dias * self.km_diarios())

    def km_restantes_estimados(self):
        if not self.km_proximo_mantenimiento:
            return None
        return self.km_proximo_mantenimiento - self.km_estimados_hoy()

    def dias_restantes_mantenimiento(self):
        if not self.fecha_proximo_mantenimiento:
            return None
        return (self.fecha_proximo_mantenimiento - timezone.now().date()).days

    def estado_mantenimiento(self):
        """Revisa km Y fecha — lo que llegue primero."""
        km_rest  = self.km_restantes_estimados()
        dias_rest = self.dias_restantes_mantenimiento()

        vencido_km   = km_rest is not None and km_rest <= 0
        vencido_fecha = dias_rest is not None and dias_rest <= 0

        if vencido_km or vencido_fecha:
            return 'vencido'

        alerta_km   = km_rest is not None and km_rest <= self.km_alerta_anticipacion
        alerta_fecha = dias_rest is not None and dias_rest <= 15  

        if alerta_km or alerta_fecha:
            return 'alerta'

        return 'ok'

    def __str__(self):
        return f"{self.placa} - {self.modelo} ({self.marca.nombre})"

    class Meta:
        db_table = 'vehiculo'


# ══════════════════════════════════════════════════════════
#  NOTIFICACION
# ══════════════════════════════════════════════════════════
def validar_no_futuro(value):
    anio_actual = timezone.now().year
    if value.year > anio_actual:
        raise ValidationError(
            f"No se permiten notificaciones para años futuros. El año máximo permitido es {anio_actual}."
        )

class Notificacion(models.Model):
    TIPOS = [
        ('Alerta', 'Alerta'), 
        ('Recordatorio', 'Recordatorio'), 
        ('Mantenimiento', 'Mantenimiento'), 
        ('Urgente', 'Urgente'), 
        ('Informacion', 'Información')
    ]
    ORIGENES = [
        ('SISTEMA', 'Automática del sistema'), 
        ('ADMIN', 'Creada por administrador')
    ]
    
    tipo     = models.CharField(max_length=50, choices=TIPOS)
    origen   = models.CharField(max_length=10, choices=ORIGENES, default='ADMIN')
    titulo   = models.CharField(max_length=150, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    mensaje  = models.TextField()
    leido    = models.BooleanField(default=False)
    
    # 2. Aplicamos DateField con el validador personalizado
    # Esto permite que sea editable en el formulario y bloquea años futuros
    fecha    = models.DateField(
        default=timezone.now, 
        validators=[validar_no_futuro],
        help_text="Seleccione la fecha de la notificación (no mayor al año actual)."
    )

    def __str__(self):
        return f"[{self.get_origen_display()}] {self.tipo} — {self.titulo or self.mensaje[:40]}"

    class Meta:
        db_table = 'notificacion'
        ordering = ['-fecha']

# ══════════════════════════════════════════════════════════
#  ORDEN DE SERVICIO
# ══════════════════════════════════════════════════════════
class OrdenServicio(models.Model):
    ESTADOS = [('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Terminado', 'Terminado')]
    empleado  = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    vehiculo  = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(TipoServicio, verbose_name="Servicios")
    fecha     = models.DateTimeField(default=timezone.now)
    km_actual = models.IntegerField()
    estado    = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._actualizar_km_vehiculo()

    def _actualizar_km_vehiculo(self):
        veh = self.vehiculo
        if self.km_actual >= veh.km_ultimo_servicio:
            veh.km_ultimo_servicio = self.km_actual
            veh.fecha_ultimo_servicio = self.fecha.date()
        servs = self.servicios.filter(intervalo_km__gt=0)
        if servs.exists():
            menor = servs.order_by('intervalo_km').first().intervalo_km
            veh.km_proximo_mantenimiento = veh.km_ultimo_servicio + menor
        veh.save(update_fields=['km_ultimo_servicio', 'km_proximo_mantenimiento', 'fecha_ultimo_servicio'])

    def __str__(self):
        return f"Orden #{self.id} — {self.vehiculo.placa}"

    class Meta:
        db_table = 'orden_servicio'


# ══════════════════════════════════════════════════════════
#  COMPRA (Sin lógica de stock, delegada a signals)
# ══════════════════════════════════════════════════════════
class Compra(models.Model):
    METODOS = [('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia'), ('Credito', 'Crédito')]
    proveedor             = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto              = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad              = models.IntegerField()
    fecha                 = models.DateTimeField(default=timezone.now)
    num_factura_proveedor = models.CharField(max_length=50, unique=True)
    metodo_pago           = models.CharField(max_length=20, choices=METODOS, default='Efectivo')
    total_pagado          = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk and self.metodo_pago != 'Credito':
            Caja.objects.create(
                descripcion = f"Compra Factura {self.num_factura_proveedor}",
                monto       = self.total_pagado,
                tipo        = 'EGRESO',
                categoria   = 'Proveedores',
                metodo_pago = self.metodo_pago,
            )
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'compra'


# ══════════════════════════════════════════════════════════
#  DETALLE ORDEN (Sin lógica de stock, delegada a signals)
# ══════════════════════════════════════════════════════════
class DetalleOrdenProducto(models.Model):
    orden    = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name='productos_usados')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.producto.stock < self.cantidad:
                raise ValidationError(f"Stock insuficiente para '{self.producto.nombre}'.")
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'detalle_orden_producto'


# ══════════════════════════════════════════════════════════
#  FACTURA
# ══════════════════════════════════════════════════════════
class Factura(models.Model):
    TIPO_FACTURA = [('SERVICIO', 'Orden de Servicio'), ('PRODUCTO', 'Venta de Producto')]
    METODOS_PAGO = [('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia'), ('TarjetaDebito', 'Tarjeta Débito'), ('Nequi', 'Nequi'), ('Daviplata', 'Daviplata')]
    ESTADOS_PAGO = [('Pendiente', 'Pendiente'), ('Pagada', 'Pagada')]

    tipo           = models.CharField(max_length=10, choices=TIPO_FACTURA, default='SERVICIO')
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision  = models.DateTimeField(auto_now_add=True)
    orden_servicio = models.ForeignKey(OrdenServicio, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal       = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # ← nuevo
    iva            = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # ← nuevo
    total          = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado_pago    = models.CharField(max_length=10, choices=ESTADOS_PAGO, default='Pendiente')
    metodo_pago    = models.CharField(max_length=20, choices=METODOS_PAGO, null=True, blank=True)  # ← agregué choices
    fecha_pago     = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.estado_pago == 'Pagada' and not self.fecha_pago:
            self.fecha_pago = timezone.now()
        super().save(*args, **kwargs)
        if self.estado_pago == 'Pagada':
            if not Caja.objects.filter(descripcion__icontains=self.numero_factura).exists():
                Caja.objects.create(
                    descripcion = f"Factura {self.numero_factura}",
                    monto       = self.total,
                    tipo        = 'INGRESO',
                    categoria   = 'Ventas' if self.tipo == 'PRODUCTO' else 'Servicios',
                    metodo_pago = self.metodo_pago or 'Efectivo',
                )
            if self.tipo == 'SERVICIO' and self.orden_servicio:
                self.orden_servicio.estado = 'Terminado'
                self.orden_servicio.save()

    class Meta:
        db_table = 'factura'
        ordering = ['-fecha_emision']