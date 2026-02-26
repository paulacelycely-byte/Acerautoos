import re
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from app.models import (
    Categoria, Entrada_Vehiculo, Ventas, Usuario, 
    Proveedor, tipo_servicio, Compra, Factura, 
    Salida_Vehiculo, insumo, Servicio, Producto, 
    Vehiculo, Cliente, Notificacion
)

# --- VALIDACIONES ---
def validar_solo_letras(valor):
    if any(char.isdigit() for char in valor):
        raise forms.ValidationError("Este campo no puede contener números.")

# --- FORMULARIOS ---

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

class Entrada_vehiculoForm(forms.ModelForm):
    class Meta:
        model = Entrada_Vehiculo
        fields = '__all__'
        widgets = {
            'documento': forms.NumberInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_hora_entrada': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class VentasForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = ['fecha', 'documento', 'cliente', 'usuario', 'productos', 'salida', 'total']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'documento': forms.TextInput(attrs={'placeholder': 'Documento', 'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'productos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'salida': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total'].required = False

    def clean_total(self):
        total = self.cleaned_data.get('total')
        return total if total else 0

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TipoServicioForm(ModelForm):
    class Meta:
        model = tipo_servicio
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_entrada_estimada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_salida_estimada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductosForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'

class Salida_VehiculoForm(ModelForm):
    class Meta:
        model = Salida_Vehiculo
        fields = '__all__'
        widgets = {
            'fecha_hora_salida': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class InsumoForm(ModelForm):
    class Meta:
        model = insumo
        fields = '__all__'

class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'

class NotificacionForm(ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'