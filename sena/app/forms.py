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

        if len(descripcion) > 100:
            raise forms.ValidationError('La descripcion no puede exceder los 100 caracteres')

        # VALIDACION AGREGADA
        if not re.match(r'^[a-zA-Z0-9\s.,]+$', descripcion):
            raise forms.ValidationError('La descripcion contiene caracteres no permitidos')

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

    # VALIDACION MEJORADA
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener mínimo 3 caracteres')

        # AGREGADO: solo letras
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')

        return nombre


    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')

        if len(descripcion) < 5:
            raise forms.ValidationError('La descripcion debe tener mínimo 5 caracteres')

        # AGREGADO
        if not re.match(r'^[a-zA-Z0-9\s.,]+$', descripcion):
            raise forms.ValidationError('La descripcion contiene caracteres no permitidos')

        return descripcion


    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')

        return precio


    # VALIDACION NUEVA (MUY IMPORTANTE)
    def clean_existencia(self):
        existencia = self.cleaned_data.get('existencia')

        if existencia < 0:
            raise forms.ValidationError('La existencia no puede ser negativa')

        return existencia




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

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')

        if not re.match(r'^[A-Z0-9]+$', placa):
            raise forms.ValidationError('La placa solo puede contener letras mayúsculas y números')

        return placa


    def clean_kilometraje(self):
        kilometraje = self.cleaned_data.get('kilometraje')

        if kilometraje < 0:
            raise forms.ValidationError('El kilometraje no puede ser negativo')

        return kilometraje


    def clean_documento(self):
        documento = self.cleaned_data.get('documento')

        if not documento.isdigit():
            raise forms.ValidationError('El documento solo puede contener números')

        return documento




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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras')

        return nombre


    def clean_documento(self):
        documento = self.cleaned_data.get('documento')

        if not documento.isdigit():
            raise forms.ValidationError('El documento solo puede contener números')

        return documento




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

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')

        if len(titulo) < 5:
            raise forms.ValidationError('El titulo debe tener mínimo 5 caracteres')

        return titulo


    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')

        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener mínimo 10 caracteres')

        return mensaje