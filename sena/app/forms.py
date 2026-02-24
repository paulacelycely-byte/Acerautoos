from django import forms
from django.forms import ModelForm
from app.models import Categorias, Proveedor, tipo_servicio, Compra ,Factura

# --- FUNCIONES DE VALIDACIÓN ---
def validar_solo_letras(valor):
    if any(char.isdigit() for char in valor):
        raise forms.ValidationError("Este campo no puede contener números.")
    if valor and valor.strip() == "0":
        raise forms.ValidationError("El valor no puede ser solo '0'.")

# --- FORMULARIOS ---

class CategoriaForm(ModelForm):
    class Meta:
        model = Categorias
        fields = '__all__'
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la categoria'}),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripcion de la categoria',
                'rows': 3,
            }),
        }

    def clean_nombre_categoria(self):
        nombre = self.cleaned_data.get('nombre_categoria')
        validar_solo_letras(nombre)
        return nombre

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        validar_solo_letras(nombre)
        return nombre

class TipoServicioForm(ModelForm):
    class Meta:
        model = tipo_servicio
        fields = ['nombre', 'descripcion', 'categoria', 'hora_entrada_estimada', 'hora_salida_estimada', 'estado']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del servicio', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción', 'rows': 3, 'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Categoría', 'class': 'form-control'}),
            'hora_entrada_estimada': forms.TimeInput(attrs={'class': 'form-control border-left-0', 'type': 'time'}),
            'hora_salida_estimada': forms.TimeInput(attrs={'class': 'form-control border-left-0', 'type': 'time'}),
            'estado': forms.CheckboxInput(attrs={'class': 'custom-control-input'})
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) < 3:
            raise forms.ValidationError("El nombre es muy corto.")
        validar_solo_letras(nombre)
        return nombre

    def clean_categoria(self):
        cat = self.cleaned_data.get('categoria')
        validar_solo_letras(cat)
        return cat

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get("hora_entrada_estimada")
        salida = cleaned_data.get("hora_salida_estimada")
        if entrada and salida:
            if salida <= entrada:
                self.add_error('hora_salida_estimada', "La hora de salida debe ser posterior a la de entrada.")
        return cleaned_data

# --- NUEVO FORMULARIO DE COMPRA ---
class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        
        # Aquí quitamos el "fk_" de las etiquetas
        labels = {
            'fecha': 'Fecha de Compra',
            'fk_proveedor': 'Proveedor',
            'fk_insumo': 'Insumo',
            'total': 'Total a Pagar',
            'estado': 'Estado del Pedido'
        }

        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date' # Esto pone el CALENDARIO automático
            }),
            'fk_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'fk_insumo': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'estado': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Pendiente', 'Pendiente'),
                ('Completado', 'Completado'),
                ('Cancelado', 'Cancelado'),
            ]),
        }

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is not None and total < 0:
            raise forms.ValidationError("El precio total no puede ser negativo.")
        return total

class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        labels = {
            'venta': 'Venta Asociada',
            'subtotal': 'Subtotal',
            'iva': 'IVA (19%)',
            'total': 'Total Facturado',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'venta': forms.Select(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }