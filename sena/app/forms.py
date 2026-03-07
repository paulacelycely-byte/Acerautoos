from django import forms
import re
from datetime import date
from django.utils import timezone
from .models import (
    Proveedor, Producto, Compra, Cliente, Marca, Vehiculo,
    TipoServicio, OrdenServicio, VentasFactura, Usuario,
    Notificacion, Caja, DetalleOrdenProducto, CompatibilidadProducto
)


# ══════════════════════════════════════════════════════════
#  UTILIDADES COMPARTIDAS
# ══════════════════════════════════════════════════════════

def val_solo_letras(valor, campo):
    """Solo letras, tildes, ñ y espacios."""
    if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', str(valor).strip()):
        raise forms.ValidationError(f"'{campo}' solo permite letras y espacios, sin números ni símbolos.")
    return valor.strip()

def val_solo_numeros(valor, campo):
    """Solo dígitos 0-9."""
    limpio = str(valor).strip()
    if not limpio.isdigit():
        raise forms.ValidationError(f"'{campo}' solo permite números, sin letras ni símbolos.")
    return limpio

def val_placa_colombiana(valor):
    """Formato colombiano estricto. Carro: ABC123 — Moto: ABC12D"""
    placa = str(valor).strip().upper().replace(" ", "")
    if not (re.match(r'^[A-Z]{3}[0-9]{3}$', placa) or re.match(r'^[A-Z]{3}[0-9]{2}[A-Z]{1}$', placa)):
        raise forms.ValidationError("Placa inválida. Use el formato ABC123 (carro) o ABC12D (moto).")
    return placa

def val_no_negativo(valor, campo):
    if valor < 0:
        raise forms.ValidationError(f"'{campo}' no puede ser un valor negativo.")
    return valor

def val_positivo(valor, campo):
    if valor <= 0:
        raise forms.ValidationError(f"'{campo}' debe ser mayor que 0.")
    return valor

def val_email(valor, campo):
    if not re.match(r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$', str(valor).strip()):
        raise forms.ValidationError(f"'{campo}' no tiene un formato de correo válido. Ej: correo@dominio.com")
    return valor.strip().lower()

def val_telefono_colombiano(valor, campo):
    limpio = str(valor).strip()
    if not limpio.isdigit():
        raise forms.ValidationError(
            f"'{campo}' solo permite números, sin espacios, guiones ni símbolos."
        )
    if len(limpio) == 10:
        if limpio.startswith('3'):
            return limpio
        elif limpio.startswith('60') or limpio.startswith('61'):
            return limpio
        else:
            raise forms.ValidationError(
                f"'{campo}': celular debe empezar por 3 (ej: 3107928076) "
                f"o fijo con indicativo por 60/61 (ej: 6012345678)."
            )
    elif len(limpio) == 7:
        return limpio
    else:
        raise forms.ValidationError(
            f"'{campo}' inválido. Use 10 dígitos para celular (ej: 3107928076) "
            f"o 7 dígitos para fijo local (ej: 2345678). "
            f"Recibido: {len(limpio)} dígitos."
        )

def val_documento_colombiano(valor, campo, tipo_doc=None):
    limpio = str(valor).strip()
    if tipo_doc == 'NIT':
        if not limpio.isdigit() or not (9 <= len(limpio) <= 10):
            raise forms.ValidationError(f"'{campo}': NIT debe tener 9 o 10 dígitos.")
    elif tipo_doc == 'CC':
        if not limpio.isdigit() or not (6 <= len(limpio) <= 10):
            raise forms.ValidationError(f"'{campo}': Cédula debe tener entre 6 y 10 dígitos.")
    elif tipo_doc == 'CE':
        if not limpio.isdigit() or not (6 <= len(limpio) <= 7):
            raise forms.ValidationError(f"'{campo}': Cédula de extranjería debe tener 6 o 7 dígitos.")
    elif tipo_doc == 'PAS':
        if not re.match(r'^[A-Z0-9]{5,12}$', limpio.upper()):
            raise forms.ValidationError(f"'{campo}': Pasaporte debe tener entre 5 y 12 caracteres alfanuméricos.")
    else:
        if not limpio.isdigit():
            raise forms.ValidationError(f"'{campo}' solo permite números.")
    return limpio


# ══════════════════════════════════════════════════════════
#  USUARIO
# ══════════════════════════════════════════════════════════

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ['fecha_registro']

    def clean_nombres(self):
        nombres = val_solo_letras(self.cleaned_data['nombres'], "Nombres")
        if len(nombres) < 2:
            raise forms.ValidationError("'Nombres' debe tener al menos 2 caracteres.")
        return nombres

    def clean_apellidos(self):
        apellidos = val_solo_letras(self.cleaned_data['apellidos'], "Apellidos")
        if len(apellidos) < 2:
            raise forms.ValidationError("'Apellidos' debe tener al menos 2 caracteres.")
        return apellidos

    def clean_cedula(self):
        cedula = val_solo_numeros(self.cleaned_data['cedula'], "Cédula")
        if not (6 <= len(cedula) <= 10):
            raise forms.ValidationError("La cédula debe tener entre 6 y 10 dígitos.")
        qs = Usuario.objects.filter(cedula=cedula)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario registrado con esta cédula.")
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            return val_telefono_colombiano(telefono, "Teléfono")
        return telefono

    def clean_correo(self):
        correo = val_email(self.cleaned_data['correo'], "Correo")
        qs = Usuario.objects.filter(correo=correo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo.")
        return correo

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if len(password) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return password

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirmacion = cleaned.get('password_confirmacion')
        if password and confirmacion and password != confirmacion:
            self.add_error('password_confirmacion', "Las contraseñas no coinciden.")
        return cleaned


# ══════════════════════════════════════════════════════════
#  PROVEEDOR
# ══════════════════════════════════════════════════════════

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def clean_nombre(self):
        nombre = val_solo_letras(self.cleaned_data['nombre'], "Nombre del proveedor")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del proveedor debe tener al menos 3 caracteres.")
        return nombre

    def clean_nit(self):
        nit = val_solo_numeros(self.cleaned_data['nit'], "NIT")
        if not (9 <= len(nit) <= 10):
            raise forms.ValidationError("El NIT debe tener 9 o 10 dígitos.")
        qs = Proveedor.objects.filter(nit=nit)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un proveedor registrado con este NIT.")
        return nit

    def clean_telefono(self):
        telefono = val_telefono_colombiano(self.cleaned_data['telefono'], "Teléfono")
        qs = Proveedor.objects.filter(telefono=telefono)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un proveedor registrado con este teléfono.")
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if direccion and len(direccion) < 5:
            raise forms.ValidationError("La dirección es demasiado corta (mínimo 5 caracteres).")
        return direccion


# ══════════════════════════════════════════════════════════
#  MARCA  
# ══════════════════════════════════════════════════════════

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9\s\-]+$', nombre):
            raise forms.ValidationError("El nombre solo permite letras, números, espacios y guiones.")
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        qs = Marca.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Esta marca ya existe en el sistema.")
        return nombre

    def clean_pais_origen(self):
        pais = self.cleaned_data.get('pais_origen', '')
        if pais:
            pais = pais.strip()
            if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', pais):
                raise forms.ValidationError("El país solo permite letras y espacios, sin números ni símbolos.")
            if len(pais) < 3:
                raise forms.ValidationError("El nombre del país debe tener al menos 3 caracteres.")
        return pais

    def clean_descripcion(self):
        desc = self.cleaned_data.get('descripcion', '').strip()
        if desc:
            if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9\s\.,\-\(\)]+$', desc):
                raise forms.ValidationError("La descripción no permite caracteres especiales.")
            if len(desc) < 5:
                raise forms.ValidationError("La descripción es demasiado corta (mínimo 5 caracteres).")
            if len(desc) > 200:
                raise forms.ValidationError("La descripción no puede superar 200 caracteres.")
        return desc

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo and hasattr(logo, 'name'):
            ext = logo.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError("Solo se permiten imágenes JPG, PNG o WEBP.")
            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("La imagen no puede superar los 2 MB.")
        return logo


# ══════════════════════════════════════════════════════════
#  PRODUCTO
# ══════════════════════════════════════════════════════════

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def clean_codigo(self):
        codigo = val_solo_numeros(self.cleaned_data['codigo'], "Código")
        if len(codigo) < 3:
            raise forms.ValidationError("El código debe tener al menos 3 dígitos.")
        qs = Producto.objects.filter(codigo=codigo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con este código.")
        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del producto debe tener al menos 3 caracteres.")
        qs = Producto.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con este nombre.")
        return nombre

    def clean_precio(self):
        precio = val_positivo(self.cleaned_data['precio'], "Precio")
        if precio > 99999999:
            raise forms.ValidationError("El precio ingresado es demasiado alto.")
        return precio

    def clean_stock(self):
        return val_no_negativo(self.cleaned_data['stock'], "Stock")

    def clean_stock_minimo(self):
        return val_no_negativo(self.cleaned_data['stock_minimo'], "Stock mínimo")

    def clean(self):
        cleaned = super().clean()
        stock = cleaned.get('stock')
        stock_min = cleaned.get('stock_minimo')
        if stock is not None and stock_min is not None:
            if stock_min > stock:
                self.add_error('stock_minimo', "El stock mínimo no puede ser mayor al stock actual.")
        return cleaned


# ══════════════════════════════════════════════════════════
#  COMPRA
# ══════════════════════════════════════════════════════════

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'

    def clean_cantidad(self):
        cantidad = val_positivo(self.cleaned_data['cantidad'], "Cantidad")
        if cantidad > 10000:
            raise forms.ValidationError("La cantidad no puede superar 10.000 unidades por compra.")
        return cantidad

    def clean_num_factura_proveedor(self):
        nf = self.cleaned_data['num_factura_proveedor'].strip()
        if not nf:
            raise forms.ValidationError("El número de factura es obligatorio.")
        if len(nf) < 3:
            raise forms.ValidationError("El número de factura debe tener al menos 3 caracteres.")
        qs = Compra.objects.filter(num_factura_proveedor=nf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una compra registrada con este número de factura.")
        return nf

    def clean_total_pagado(self):
        total = val_no_negativo(self.cleaned_data['total_pagado'], "Total pagado")
        if total > 999999999:
            raise forms.ValidationError("El total pagado es demasiado alto. Verifique el valor.")
        return total

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > timezone.now():
            raise forms.ValidationError("La fecha de compra no puede ser una fecha futura.")
        return fecha


# ══════════════════════════════════════════════════════════
#  CLIENTE
# ══════════════════════════════════════════════════════════

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_nombre(self):
        nombre = val_solo_letras(self.cleaned_data['nombre'], "Nombre del cliente")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_numero_documento(self):
        tipo_doc = self.cleaned_data.get('tipo_documento', 'CC')
        doc = self.cleaned_data['numero_documento'].strip()
        doc = val_documento_colombiano(doc, "Número de documento", tipo_doc)
        qs = Cliente.objects.filter(numero_documento=doc)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un cliente registrado con este número de documento.")
        return doc

    def clean_telefono(self):
        telefono = val_telefono_colombiano(self.cleaned_data['telefono'], "Teléfono")
        qs = Cliente.objects.filter(telefono=telefono)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un cliente registrado con este teléfono.")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = val_email(email, "Email")
            qs = Cliente.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe un cliente registrado con este email.")
        return email


# ══════════════════════════════════════════════════════════
#  VEHÍCULO
# ══════════════════════════════════════════════════════════

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

    def clean_placa(self):
        placa = val_placa_colombiana(self.cleaned_data['placa'])
        qs = Vehiculo.objects.filter(placa=placa)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"Ya existe un vehículo registrado con la placa '{placa}'.")
        return placa

    def clean_modelo(self):
        modelo = self.cleaned_data['modelo'].strip()
        if not re.match(r'^\d{4}$', modelo):
            raise forms.ValidationError("El año debe tener exactamente 4 dígitos. Ej: 2019")
        anio = int(modelo)
        anio_actual = date.today().year
        if anio < 1900 or anio > anio_actual:
            raise forms.ValidationError(f"El año debe estar entre 1900 y {anio_actual}.")
        return modelo


# ══════════════════════════════════════════════════════════
#  TIPO DE SERVICIO
# ══════════════════════════════════════════════════════════

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del servicio debe tener al menos 3 caracteres.")
        qs = TipoServicio.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un tipo de servicio con este nombre.")
        return nombre

    def clean_precio_mano_obra(self):
        precio = val_positivo(self.cleaned_data['precio_mano_obra'], "Precio de mano de obra")
        if precio > 99999999:
            raise forms.ValidationError("El precio de mano de obra es demasiado alto.")
        return precio


# ══════════════════════════════════════════════════════════
#  ORDEN DE SERVICIO
# ══════════════════════════════════════════════════════════

class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = '__all__'

    def clean_km_actual(self):
        km = self.cleaned_data['km_actual']
        if km < 0:
            raise forms.ValidationError("El kilometraje no puede ser negativo.")
        if km > 1000000:
            raise forms.ValidationError("El kilometraje ingresado es demasiado alto (máx. 1.000.000 km).")
        return km

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > timezone.now():
            raise forms.ValidationError("La fecha de la orden no puede ser una fecha futura.")
        return fecha


# ══════════════════════════════════════════════════════════
#  DETALLE ORDEN PRODUCTO
# ══════════════════════════════════════════════════════════

class DetalleOrdenProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenProducto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0, estado=True)

    def clean_cantidad(self):
        cantidad = val_positivo(self.cleaned_data['cantidad'], "Cantidad")
        if cantidad > 1000:
            raise forms.ValidationError("La cantidad no puede superar 1.000 unidades por detalle.")
        return cantidad

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        cantidad = cleaned.get('cantidad')
        if producto and cantidad:
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f"Stock insuficiente para '{producto.nombre}'. "
                    f"Disponible: {producto.stock}, solicitado: {cantidad}."
                )
        return cleaned


# ══════════════════════════════════════════════════════════
#  VENTAS / FACTURA
# ══════════════════════════════════════════════════════════

class VentasFacturaForm(forms.ModelForm):
    class Meta:
        model = VentasFactura
        fields = '__all__'

    def clean_numero_factura(self):
        nf = self.cleaned_data['numero_factura'].strip()
        if not nf:
            raise forms.ValidationError("El número de factura es obligatorio.")
        if len(nf) < 3:
            raise forms.ValidationError("El número de factura debe tener al menos 3 caracteres.")
        qs = VentasFactura.objects.filter(numero_factura=nf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una factura de venta con este número.")
        return nf

    def clean_total(self):
        total = val_no_negativo(self.cleaned_data['total'], "Total de factura")
        if total > 999999999:
            raise forms.ValidationError("El total de la factura es demasiado alto. Verifique el valor.")
        return total


# ══════════════════════════════════════════════════════════
#  CAJA
# ══════════════════════════════════════════════════════════

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = '__all__'

    def clean_monto(self):
        monto = val_positivo(self.cleaned_data['monto'], "Monto")
        if monto > 999999999:
            raise forms.ValidationError("El monto es demasiado alto. Verifique el valor.")
        return monto

    def clean_descripcion(self):
        desc = self.cleaned_data['descripcion'].strip()
        if len(desc) < 5:
            raise forms.ValidationError("La descripción es demasiado corta (mínimo 5 caracteres).")
        if len(desc) > 255:
            raise forms.ValidationError("La descripción no puede superar 255 caracteres.")
        return desc

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > timezone.now():
            raise forms.ValidationError("La fecha del movimiento no puede ser una fecha futura.")
        return fecha

    def clean_comprobante(self):
        archivo = self.cleaned_data.get('comprobante')
        if archivo:
            ext = archivo.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Solo se permiten archivos PDF, JPG o PNG.")
            if archivo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("El archivo no puede superar los 5 MB.")
        return archivo

    def clean_observaciones(self):
        obs = self.cleaned_data.get('observaciones', '').strip()
        if obs and len(obs) < 10:
            raise forms.ValidationError("Las observaciones son demasiado cortas (mínimo 10 caracteres).")
        return obs or None


# ══════════════════════════════════════════════════════════
#  NOTIFICACIÓN
# ══════════════════════════════════════════════════════════

class NotificacionForm(forms.ModelForm):
    TIPOS_NOTIFICACION = [
        ('',            '-- Seleccione un tipo --'),
        ('Alerta',        'Alerta'),
        ('Recordatorio',  'Recordatorio'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Urgente',       'Urgente'),
        ('Informacion',   'Información'),
    ]

    tipo = forms.ChoiceField(
        choices=TIPOS_NOTIFICACION,
        label="Tipo de Notificación",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Notificacion
        fields = '__all__'

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if not tipo:
            raise forms.ValidationError("Seleccione un tipo de notificación.")
        tipos_validos = [t[0] for t in self.TIPOS_NOTIFICACION if t[0]]
        if tipo not in tipos_validos:
            raise forms.ValidationError("Tipo de notificación no válido.")
        return tipo

    def clean_mensaje(self):
        msg = self.cleaned_data['mensaje'].strip()
        if len(msg) < 10:
            raise forms.ValidationError("El mensaje es demasiado corto (mínimo 10 caracteres).")
        if len(msg) > 500:
            raise forms.ValidationError("El mensaje no puede superar 500 caracteres.")
        return msg


# ══════════════════════════════════════════════════════════
#  COMPATIBILIDAD PRODUCTO
# ══════════════════════════════════════════════════════════

class CompatibilidadProductoForm(forms.ModelForm):
    class Meta:
        model = CompatibilidadProducto
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        marca_vehiculo = cleaned.get('marca_vehiculo')
        if producto and marca_vehiculo:
            qs = CompatibilidadProducto.objects.filter(
                producto=producto,
                marca_vehiculo=marca_vehiculo
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    f"Ya existe la compatibilidad entre '{producto.nombre}' "
                    f"y la marca '{marca_vehiculo.nombre}'."
                )
        return cleaned