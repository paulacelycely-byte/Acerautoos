from django.db import models
from datetime import datetime
from decimal import Decimal

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre  
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias" 
        db_table = "categoria"   

#-producto model---------
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos')   

    def __str__(self):
        return self.nombre  
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos" 
        db_table = "Producto"


#----------cliente model------
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    cedula = models.CharField(max_length=20, verbose_name="cedula")    
    fecha_nacimiento = models.DateField(default=datetime.now, verbose_name="Fecha de nacimiento")    
    direccion = models.TextField(max_length=150, null=True, blank=True, verbose_name="Direccion")  
    sexo = models.CharField(max_length=10, default="masculino", verbose_name="Sexo")
    

    def __str__(self):
        return self.nombre  
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes" 
        db_table = "Cliente"


#---------venta model--------
class Venta(models.Model):
    clientes = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=Decimal("0.00"), max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=Decimal("0.00"), max_digits=9, decimal_places=2)
    total = models.DecimalField(default=Decimal("0.00"), max_digits=9, decimal_places=2)


    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas" 
        db_table = "Venta"
        
#-------detalle venta model-----
class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    fk_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(default=Decimal("0.00"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id  
    
    class Meta:
        verbose_name = "DetalleVenta"
        verbose_name_plural = "DetalleVentas" 
        db_table = "DetalleVenta"
        #ordering = ['id']
        
