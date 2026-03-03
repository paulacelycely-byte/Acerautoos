from datetime import timedelta
from django.db import models
from datetime import datetime
from decimal import Decimal
from app.models import *
from django.db.models import Sum


class Usuario(models.Model):
    ROL = [(
        'Administrador', 'Administrador'
    ), ('Usuario', 'Usuario')]
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=45, choices=ROL)
    telefono = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    direccion = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

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
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "Producto"
        



class Vehiculo(models.Model):
    TIPO = [
        ('Sedán', 'Sedán'),
        ('SUV', 'SUV'),
        ('Hatchback', 'Hatchback'),
        ('Coupé', 'Coupé'),
        ('Convertible', 'Convertible'),
        ('Pickup', 'Pickup'),
        ('Minivan', 'Minivan'),
        ('Station Wagon', 'Station Wagon'),
        ('Deportivo', 'Deportivo'),
        ('Crossover', 'Crossover'),
    ]
    tipo_vehiculo = models.CharField(max_length=100,choices=TIPO)
    placa = models.CharField(max_length=6)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    kilometraje = models.IntegerField()
    documento = models.ForeignKey('Cliente',on_delete=models.CASCADE)
    modelo = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.marca} {self.modelo}"

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"
        db_table = "Vehiculo"


class insumo(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # Corregido: Se usa _str_. Retorna una sola cadena.
        return f"{self.nombre} (${self.precio_unitario})"

    class Meta:
        verbose_name = "insumo"
        verbose_name_plural = "insumos"
        db_table = "insumo"


class tipo_servicio(models.Model):
    CATEGORIAS = [
        ('MEC', 'Mecánica general'),
        ('ELEC', 'Electricidad automotriz'),
        ('FREN', 'Frenos'),
        ('SUSP', 'Suspensión'),
        ('MANT', 'Mantenimiento'),
        ('DIAG', 'Diagnóstico'),
        ('CLIM', 'Climatización'),
        ('EST', 'Estética vehicular'),
    ]
    SERVICIOS = [
        ('ACEITE', 'Cambio de aceite'),
        ('FILTROS', 'Cambio de filtros'),
        ('REVISION', 'Revisión general'),
        ('DIAGNOSTICO', 'Diagnóstico'),
        ('PREVENTIVO', 'Mantenimiento preventivo'),
        ('CORRECTIVO', 'Mantenimiento correctivo'),
        ('ALINEACION', 'Alineación y balanceo'),
        ('FRENOS', 'Servicio de frenos'),
        ('BATERIA', 'Cambio de batería'),
        ('ELECTRICO', 'Sistema eléctrico'),
        ('SUSPENSION', 'Suspensión'),
        ('DIRECCION', 'Dirección'),
        ('MOTOR', 'Reparación de motor'),
        ('SINCRONIZACION', 'Sincronización'),
        ('CORREA', 'Cambio de correa'),
        ('REFRIGERACION', 'Refrigeración'),
        ('AIRE', 'Aire acondicionado'),
        ('BUJIAS', 'Cambio de bujías'),
        ('LAVADO', 'Lavado'),
        ('INSPECCION', 'Inspección'),
    ]
    nombre = models.CharField(max_length=100, choices=SERVICIOS)
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipo_servicio"
        verbose_name_plural = "tipo_servicios"
        db_table = "tipo_servicio"


class Entrada_vehiculo(models.Model):

    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
    ]

    tipo_documento = models.CharField(
        max_length=2,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name="Tipo de documento"
    )

    documento = models.IntegerField(unique=True)

    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)

    placa = models.CharField(max_length=6)


    

    def __str__(self):
        return f"Entrada {self.placa} - {self.fecha_hora_entrada}"

    class Meta:
        db_table = "entrada_vehiculos"
        verbose_name = "Entrada de Vehículo"
        verbose_name_plural = "Entradas de Vehículos"


estado = [
    (True, 'Activo'),
    (False, 'Inactivo'),

]


class Proveedor(models.Model):
    estado = [
            (True, 'Activo'),
            (False, 'Inactivo'),
        ]
    nombre = models.CharField(max_length=50)
    documento = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True, choices=estado)
    mercancia = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "Proveedor"


class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10)

    fk_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fk_insumo = models.ForeignKey(insumo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compra {self.id_compra} - {self.estado}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        db_table = "compra"


class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    fk_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        db_table = "categoria_productos"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f" {self.nombre}-{str(self.documento)}"

    class Meta:
        db_table = "Cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Ventas(models.Model):
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    documento = models.CharField(max_length=10)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    salida = models.ForeignKey('Salida_Vehiculo', on_delete=models.CASCADE)
    # Correcto: 'Producto'
    productos = models.ManyToManyField(Producto)
    # Correcto: 'Usuario'
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        # Corregido: Retorna una sola cadena.
        return f"Venta del {self.fecha} a {self.cliente} {self.salida}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Venta"
        db_table = "Venta"


# --- MODELOS CON RELACIONES ---


class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10)

    # CORREGIDO: 'Proveedor' -> 'Proveedores' (Nombre de la clase)
    fk_proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    # CORREGIDO: 'Insumo' -> 'insumo' (Nombre de la clase)
    fk_insumo = models.ForeignKey('insumo', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.fk_insumo:
            self.total = self.fk_insumo.precio_unitario * self.fk_insumo.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
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

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        verbose_name = "Categoría "
        verbose_name_plural = "Categorías"
        db_table = "categoria"


entrada = [
    (True, 'Entrada'),
    (False, 'Salida'),
]


class Salida_vehiculo(models.Model):
    entrada = models.OneToOneField(
        'Entrada_Vehiculo',
        on_delete=models.CASCADE,
        related_name="salida"
    )

    fecha_hora_salida = models.DateTimeField()
    total_a_pagar = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True
    )

    # 🔹 Duración total del vehículo en el taller
    @property
    def duracion_total(self):
        return self.fecha_hora_salida - self.entrada.fecha_hora_entrada

    # 🔹 Duración formateada bonita
    def duracion_formateada(self):
        duracion = self.duracion_total
        horas = duracion.days * 24 + duracion.seconds // 3600
        minutos = (duracion.seconds % 3600) // 60
        return f"{horas}h {minutos}m"

    # 🔹 Calcular total automáticamente
    def calcular_total(self):
        total = self.entrada.servicios.aggregate(
            total=Sum('precio')
        )['total']
        return total or 0

    def save(self, *args, **kwargs):
        self.total_a_pagar = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salida {self.entrada.placa} - ${self.total_a_pagar}"

    class Meta:
        db_table = "salida_vehiculos"
        verbose_name = "Salida de Vehículo"
        verbose_name_plural = "Salidas de Vehículos"


# --- MODELO AUXILIAR FALTANTE (Agregado) ---
# Se asume la existencia del modelo Cliente ya que Ventas lo necesita.


class Factura(models.Model):
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    venta = models.ForeignKey('Ventas', on_delete=models.CASCADE)

    def __str__(self):
        return f"Factura #{self.id} por ${self.total}"

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        db_table = "Factura"


class Notificacion(models.Model):
    TIPO_NOTIFICACION = [
        ('Mensaje', 'Mensaje General'),      # Para cualquier comunicación normal
        ('Alerta', 'Alerta Importante'),     # Requiere atención inmediata
        ('Recordatorio', 'Recordatorio'),   # Para avisos o eventos próximos
    ]
    id_notificacion = models.AutoField(primary_key=True)
    tipo_notificacion = models.CharField(choices=TIPO_NOTIFICACION)
    mensaje = models.CharField(max_length=45)
    fecha_envio = models.CharField(max_length=45)
    ventas = models.ForeignKey('Ventas', on_delete=models.CASCADE)

    def __str__(self):
        return f"Notificación {self.id_notificacion} - {self.mensaje}"

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        db_table = "notificacion"


class Servicio(models.Model):
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    entrada = models.ForeignKey(
        'Entrada_vehiculo',
        on_delete=models.CASCADE,
        related_name="servicios"
    )

    insumo = models.ForeignKey(
        'insumo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    tipo_servicio = models.ForeignKey(
        'tipo_servicio',
        on_delete=models.CASCADE
    )
    def save(self, *args, **kwargs):
        if self.insumo:
            self.precio += self.insumo.precio_unitario
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.descripcion} - ${self.precio}"

    class Meta:
        db_table = "servicios"
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"