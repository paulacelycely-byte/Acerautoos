from django import forms
import re
from django.utils import timezone
from .models import (
    Proveedor, Producto, Compra, Cliente, 
    Marca, Vehiculo, TipoServicio, OrdenServicio, VentasFactura, Usuario, Notificacion,Caja,DetalleOrdenProducto
)

# =========================================================
# --- UTILIDADES DE VALIDACIÓN (REUTILIZABLES) ---
# =========================================================


def validar_solo_letras(valor):
    if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', str(valor)):
        raise forms.ValidationError(
            "Este campo solo puede contener letras y espacios.")


def validar_numerico_estricto(valor, longitud=None):
    valor_str = str(valor).strip()
    if not valor_str.isdigit():
        raise forms.ValidationError(
            "Este campo debe contener solo números (sin letras, puntos o espacios).")
    if longitud and len(valor_str) != longitud:
        raise forms.ValidationError(
            f"Este campo debe tener exactamente {longitud} dígitos.")
    return valor_str

# ============================
# FORMULARIO USUARIO
# ============================
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********',
            'autocomplete': 'new-password'
        }),
    )

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'cedula', 'telefono',
                  'correo', 'password', 'cargo', 'activo']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres completos'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos completos'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3001234567'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }

    def clean_nombres(self):
        val = self.cleaned_data.get('nombres', '').strip()
        validar_solo_letras(val)
        return val

    def clean_apellidos(self):
        val = self.cleaned_data.get('apellidos', '').strip()
        validar_solo_letras(val)
        return val

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        validar_numerico_estricto(cedula)
        if Usuario.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esta cédula ya está registrada.")
        return cedula

    def clean_correo(self):
        email = self.cleaned_data.get('correo', '').strip().lower()
        if Usuario.objects.filter(correo=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Este correo ya está en uso por otro usuario.")
        return email

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono')
        validar_numerico_estricto(tel, longitud=10)
        if Usuario.objects.filter(telefono=tel).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Este número de teléfono ya está registrado.")
        return tel

# ============================
# FORMULARIO PROVEEDOR
# ============================
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o Razón Social'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT o Identificación'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 dígitos'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección principal'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip().upper()
        validar_solo_letras(nombre)
        if len(nombre) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        validar_numerico_estricto(nit)
        if Proveedor.objects.filter(nit=nit).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este NIT ya está registrado.")
        return nit

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono')
        validar_numerico_estricto(tel, longitud=10)
        if Proveedor.objects.filter(telefono=tel).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Este teléfono ya pertenece a otro proveedor.")
        return tel

# ============================
# FORMULARIO CLIENTE
# ============================

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'producto', 'cantidad',
                  'num_factura_proveedor', 'metodo_pago', 'total_pagado']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'num_factura_proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° de Factura'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'total_pagado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a cero.")
        return cantidad

    def clean_total_pagado(self):
        total = self.cleaned_data.get('total_pagado')
        if total is not None and total < 0:
            raise forms.ValidationError(
                "El total pagado no puede ser negativo.")
        return total

    def clean_num_factura_proveedor(self):
        factura = self.cleaned_data.get(
            'num_factura_proveedor', '').strip().upper()
        if Compra.objects.filter(num_factura_proveedor=factura).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Este número de factura ya fue ingresado.")
        return factura


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 dígitos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        validar_solo_letras(nombre)
        return nombre

    def clean_numero_documento(self):
        doc = self.cleaned_data.get('numero_documento')
        validar_numerico_estricto(doc)
        if Cliente.objects.filter(numero_documento=doc).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Este número de documento ya está registrado.")
        return doc

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono')
        validar_numerico_estricto(tel, longitud=10)
        if Cliente.objects.filter(telefono=tel).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Este número de teléfono ya pertenece a otro cliente.")
        return tel

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if email:
            if Cliente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    "Este correo electrónico ya está registrado con otro cliente.")
        return email


class DetalleOrdenProductoForm(forms.ModelForm):

    class Meta:
        model = DetalleOrdenProducto
        fields = ['orden', 'producto', 'cantidad']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
        }


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['producto'].queryset = Producto.objects.filter(
                stock__gt=0)
            self.fields['cantidad'].widget.attrs.update({'min': 1})
            self.fields['orden'].queryset = OrdenServicio.objects.all().order_by(
                '-fecha')

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')

        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")

        return cantidad

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'pais_origen', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Toyota'}),
            'pais_origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Japón (Opcional)'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción opcional'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre.capitalize()

# ============================
# FORMULARIO PRODUCTO
# ============================
class ProductoForm(forms.ModelForm):
    estado = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'})
    )
    class Meta:
            model = Producto
            fields = '__all__'
            widgets = {
                'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Filtro de Aceite'}),
                'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detalles del repuesto'}),
                'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único'}),
                'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
                'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
                'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
                'marca': forms.Select(attrs={'class': 'form-control'}),
                'estado': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            }

    def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre', '').strip().title()
            if len(nombre) < 3:
                raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
            if Producto.objects.filter(nombre=nombre).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Ya existe un producto con este nombre.")
            return nombre

    def clean_codigo(self):
            codigo = self.cleaned_data.get('codigo', '').strip().upper()
            if codigo and len(codigo) < 4:
                raise forms.ValidationError("El código debe tener mínimo 4 caracteres.")
            if Producto.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Ya existe un producto con este código.")
            return codigo

    def clean_precio(self):
            precio = self.cleaned_data.get('precio')
            if precio is not None and precio <= 0:
                raise forms.ValidationError("El precio debe ser mayor a cero.")
            return precio

    def clean_stock(self):
            stock = self.cleaned_data.get('stock')
            if stock is not None and stock < 0:
                raise forms.ValidationError("El stock no puede ser negativo.")
            return stock

    def clean_stock_minimo(self):
            stock_minimo = self.cleaned_data.get('stock_minimo')
            stock = self.cleaned_data.get('stock')
            if stock_minimo is not None and stock_minimo < 0:
                raise forms.ValidationError("El stock mínimo no puede ser negativo.")
            if stock_minimo is not None and stock is not None and stock_minimo > stock:
                raise forms.ValidationError("El stock mínimo no puede ser mayor que la existencia actual.")
            return stock_minimo

# ============================
# FORMULARIO VEHICULO
# ============================
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Año'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa', '').upper().strip()
        if not re.match(r'^[A-Z]{3}[0-9]{3}$', placa):
            raise forms.ValidationError(
                "Formato de placa inválido (Debe ser AAA111).")
        if Vehiculo.objects.filter(placa=placa).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este vehículo ya existe.")
        return placa

    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo')
        validar_numerico_estricto(modelo, longitud=4)
        anio_actual = timezone.now().year
        if int(modelo) < 1900 or int(modelo) > (anio_actual + 1):
            raise forms.ValidationError(f"Año fuera de rango (1900 - {anio_actual + 1}).")
        return modelo
    
    
class VentasFacturaForm(forms.ModelForm):

    class Meta:
        model = VentasFactura
        fields = ['venta', 'numero_factura', 'metodo_pago', 'total']
        widgets = {
            'venta': forms.Select(attrs={'class': 'form-control'}),
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: FAC-001'
            }),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }
    def clean_numero_factura(self):
        numero = self.cleaned_data.get('numero_factura')

        existe = VentasFactura.objects.filter(
            numero_factura__iexact=numero
        ).exclude(pk=self.instance.pk).exists()

        if existe:
            raise forms.ValidationError(
                "Ya existe una factura con este número."
            )

        if not re.match(r'^[A-Za-z0-9\-]+$', numero):
            raise forms.ValidationError(
                "El número de factura solo puede contener letras, números y guiones."
            )

        return numero
    
    def clean_total(self):
        total = self.cleaned_data.get('total')

        if total <= 0:
            raise forms.ValidationError(
                "El total debe ser mayor a 0."
            )

        return total
    
    def clean_orden(self):
        orden = self.cleaned_data.get('orden')

        if VentasFactura.objects.filter(
            orden=orden
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Esta orden ya tiene una factura registrada."
            )

        return orden
    
class NotificacionForm(forms.ModelForm):

    class Meta:
        model = Notificacion
        fields = ['tipo', 'vehiculo', 'mensaje', 'leido']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba el mensaje de la notificación...'
            }),
            'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')

        if not mensaje:
            raise forms.ValidationError("El mensaje no puede estar vacío.")

        if len(mensaje) < 5:
            raise forms.ValidationError("El mensaje debe tener al menos 5 caracteres.")

        return mensaje
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        vehiculo = cleaned_data.get('vehiculo')

        if tipo == 'Mantenimiento' and not vehiculo:
            raise forms.ValidationError(
                "Debe seleccionar un vehículo para notificaciones de mantenimiento."
            )
        return cleaned_data


class OrdenServicioForm(forms.ModelForm):

    class Meta:
        model = OrdenServicio
        fields = [
            'usuario',
            'vehiculo',
            'servicio',
            'fecha',
            'km_actual',
            'km_proximo_cambio',
            'estado',
            'observaciones'
        ]
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'km_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'km_proximo_cambio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def clean_km_actual(self):
        km = self.cleaned_data.get('km_actual')
        if km is not None and km < 0:
            raise forms.ValidationError(
                "El kilometraje no puede ser negativo.")
        return km

    def clean_km_actual(self):
        km = self.cleaned_data.get('km_actual')

        if km is None:
            raise forms.ValidationError("Debe ingresar el kilometraje actual.")

        if km <= 0:
            raise forms.ValidationError("El kilometraje debe ser mayor a 0.")

        if km < 500:
            raise forms.ValidationError(
                "El kilometraje ingresado no es válido para un vehículo en servicio."
            )

        if km > 1000000:
            raise forms.ValidationError(
                "El kilometraje ingresado es demasiado alto."
            )

        return km

    def clean(self):
        cleaned_data = super().clean()
        km_actual = cleaned_data.get('km_actual')
        km_proximo = cleaned_data.get('km_proximo_cambio')
        vehiculo = cleaned_data.get('vehiculo')

        if km_actual is not None and km_proximo is not None:

            if km_proximo <= km_actual:
                self.add_error(
                    'km_proximo_cambio',
                    'El próximo cambio debe ser mayor al kilometraje actual.'
                )

            diferencia = km_proximo - km_actual

            if diferencia < 3000:
                self.add_error(
                    'km_proximo_cambio',
                    'El próximo cambio debe ser mínimo 3.000 km después.'
                )

            if diferencia > 999_999:
                self.add_error(
                    'km_proximo_cambio',
                    'El próximo cambio no puede superar 999.999 km.'
                )

        # Evitar retroceso
        if vehiculo and km_actual is not None:
            ultimo = OrdenServicio.objects.filter(
                vehiculo=vehiculo
            ).exclude(pk=self.instance.pk).order_by('-km_actual').first()

            if ultimo and km_actual < ultimo.km_actual:
                self.add_error(
                    'km_actual',
                    'No puede registrar un kilometraje menor al último registrado.'
                )

        return cleaned_data


class CajaForm(forms.ModelForm):

    class Meta:
        model = Caja
        fields = ['descripcion', 'monto', 'tipo']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del movimiento'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a 0")
        return monto

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion or len(descripcion.strip()) < 3:
            raise forms.ValidationError("La descripción es obligatoria y debe tener al menos 3 caracteres")
        return descripcion

# ============================
# FORMULARIO COMPRA 
# ============================
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a cero.")
        return cantidad
    
class TipoServicioForm(forms.ModelForm):

    class Meta:
        model = TipoServicio
        fields = ['nombre', 'precio_mano_obra']
        widgets = {
            'nombre': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del servicio'
            }),
            'precio_mano_obra': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el precio de mano de obra',
                'step': '0.01',
                'min': '0'
            }),

        }



