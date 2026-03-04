from django import forms
import re
from django.utils import timezone
from .models import (
    Proveedor, Producto, Compra, Cliente,
    Marca, Vehiculo, TipoServicio, OrdenServicio, VentasFactura, Usuario
)

# ============================
# UTILIDADES DE VALIDACIÓN
# ============================
def validar_solo_letras(valor):
    if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', str(valor)):
        raise forms.ValidationError("Este campo solo puede contener letras y espacios.")

def validar_numerico_estricto(valor, longitud=None):
    valor_str = str(valor).strip()
    if not valor_str.isdigit():
        raise forms.ValidationError("Este campo debe contener solo números (sin letras, puntos o espacios).")
    if longitud and len(valor_str) != longitud:
        raise forms.ValidationError(f"Este campo debe tener exactamente {longitud} dígitos.")
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
        fields = ['nombres', 'apellidos', 'cedula', 'telefono', 'correo', 'password', 'cargo', 'activo']
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
            raise forms.ValidationError("Este correo ya está en uso por otro usuario.")
        return email

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono')
        validar_numerico_estricto(tel, longitud=10)
        if Usuario.objects.filter(telefono=tel).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este número de teléfono ya está registrado.")
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
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
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
            raise forms.ValidationError("Este teléfono ya pertenece a otro proveedor.")
        return tel

# ============================
# FORMULARIO CLIENTE
# ============================
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
            raise forms.ValidationError("Este número de documento ya está registrado.")
        return doc

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono')
        validar_numerico_estricto(tel, longitud=10)
        if Cliente.objects.filter(telefono=tel).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este número de teléfono ya pertenece a otro cliente.")
        return tel

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if email:
            if Cliente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado con otro cliente.")
        return email

# ============================
# FORMULARIO MARCA
# ============================
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
            raise forms.ValidationError("Formato de placa inválido (Debe ser AAA111).")
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