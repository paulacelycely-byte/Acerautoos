from django import forms
from django.forms import ModelForm
from app.models import Categorias, Proveedor, tipo_servicio

class CategoriaForm(ModelForm):
    class Meta:
        model = Categorias
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la categoria'
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripcion de la categoria',
                'rows': 15,
                'cols': 17
            }),
        }

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

class TipoServicioForm(ModelForm):
    class Meta:
        model = tipo_servicio
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del tipo de servicio',
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripción del servicio',
                'rows': 3,
                'class': 'form-control'
            }),
            'categoria': forms.TextInput(attrs={
                'placeholder': 'Ingrese la categoría (ej: Mantenimiento, Reparación)',
                'class': 'form-control'
            }),
            'duracion_estimada': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nombre': 'Nombre del Servicio',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'duracion_estimada': 'Duración Estimada',
            'estado': 'Servicio Activo'
        }

    # VALIDACIÓN PARA EL NOMBRE 
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) < 3:
            raise forms.ValidationError("El nombre es muy corto. Debe tener al menos 3 caracteres.")
        return nombre

    # VALIDACIÓN PARA LA DESCRIPCIÓN
    def clean_descripcion(self):
        desc = self.cleaned_data.get('descripcion')
        if not desc:
            raise forms.ValidationError("La descripción no puede estar vacía.")
        return desc