import re
from django.forms import ModelForm
from app.models import Categorias
from app.models import Productos
from app.models import Vehiculo
from app.models import Cliente
from app.models import Notificacion

from django import forms

class CategoriasForm(ModelForm):
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
        
def clean_nombre(self):
    nombre = self.cleaned_data.get('nombre')
    if not re.match(r'^[a-zA-Z\s]+$', nombre):
        raise forms.ValidationError('El nombre solo puede contener letras y espacios')
    return nombre

def clean_descripcion(self):
    descripcion = self.cleaned_data.get('descripcion')
    if len(descripcion)>10:
        raise forms.ValidationError('La descripcion no puede exceder los 10 caracteres')
    return descripcion


class ProductosForm(ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripción del producto',
                'rows': 5
            }),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio'
            }),
        }




class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

        widgets = {

            'tipo_vehiculo': forms.TextInput(attrs={
                'placeholder': 'Ingrese el tipo de vehículo'
            }),

            'placa': forms.TextInput(attrs={
                'placeholder': 'Ingrese la placa'
            }),

            'marca': forms.TextInput(attrs={
                'placeholder': 'Ingrese la marca'
            }),

            'modelo': forms.TextInput(attrs={
                'placeholder': 'Ingrese el modelo'
            }),


            'kilometraje': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el kilometraje'
            }),

            'documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el documento'
            }),

        }

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

        widgets = {

            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del cliente',
                'autocomplete': 'off'
            }),

            'documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el documento del cliente',
                'autocomplete': 'off'
            }),

        }

class NotificacionForm(ModelForm):

    class Meta:
        model = Notificacion
        fields = '__all__'

        widgets = {

            'titulo': forms.TextInput(attrs={
                'placeholder': 'Ingrese el título de la notificación',
                'autocomplete': 'off',
                'class': 'form-control'
            }),

            'mensaje': forms.Textarea(attrs={
                'placeholder': 'Ingrese el mensaje de la notificación',
                'autocomplete': 'off',
                'class': 'form-control',
                'rows': 3
            }),

            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),

        }
        
