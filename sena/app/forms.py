import re
from django.forms import ModelForm
from app.models import Categorias
from app.models import Salida_vehiculo
from app.models import insumo
from app.models import Servicio
from django import forms  

class CategoriaForm(ModelForm):
    class Meta:
        model = Categorias
        fields = '__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={
                'placeholder':'Ingrese el nombre de la categoria '}),
            'descripcion':
            forms.Textarea(attrs={
                'placeholder':'ingrese la descripcion de la categoria ',
                'rows':15,
                'cols':17}),
        }
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El campo nombre solo puede contener letras y espacios.')
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) > 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return descripcion

        
class Salida_vehiculoForm(ModelForm):
    class Meta:
        model = Salida_vehiculo
        fields = '__all__'
        widgets = { 
            'fecha_hora_salida': forms.TimeInput(attrs={
                'type': 'datetime-local'
            }),
            'total_a_pagar': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el total a pagar'
            }),
        }
        
    def clean_fecha_hora_salida(self):
        fecha_hora_salida = self.cleaned_data.get('fecha_hora_salida')
        if not fecha_hora_salida:
            raise forms.ValidationError('La fecha y hora de salida es requerida.')
        return fecha_hora_salida
    
    
    def clean_total_a_pagar(self):
        total_a_pagar = self.cleaned_data.get('total_a_pagar')
        if total_a_pagar <= 0:
            raise forms.ValidationError('El total a pagar debe ser un número positivo.')
        return total_a_pagar
    
    def clean_entrada(self):
        entrada = self.cleaned_data.get('entrada_vehiculo')
        if not entrada:
            raise forms.ValidationError('La entrada de vehículo es requerida.')
        return entrada
        

        
class InsumoForm(ModelForm):
    class Meta:
        model = insumo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del insumo'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio unitario del insumo'
            }),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Ingrese la cantidad del insumo'
            }),
        }
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El campo nombre solo puede contener letras y espacios.')
        return nombre
    
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser un número positivo.')
        return cantidad
    
    def clean_precio_unitario(self):
        precio_unitario = self.cleaned_data.get('precio_unitario')
        if precio_unitario <= 0:
            raise forms.ValidationError('El precio unitario debe ser un número positivo.')
        return precio_unitario
    
    
    
        
class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = fields = [
            'tipo_servicio',   
            'entrada',
            'descripcion',
            'duracion',
            'precio',
            'insumo',
            'usuario',
        ]
        widgets = {
    
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripción del servicio',
                'rows': 15,
                'cols': 17
            }),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del servicio'
            }),
            'duracion': forms.TimeInput(
                format='%I:%M %p',
                attrs={
                    'type': 'time'
                }
            )
        }
     
        

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return descripcion
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser un número positivo.')
        return precio