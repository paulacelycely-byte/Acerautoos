import re
from django.forms import ModelForm
from app.models import Categorias
from app.models import Entrada_vehiculo
from django import forms
from app.models import Ventas
from app.models import Usuario
from django.utils import timezone


class CategoriaForm(ModelForm):
    class Meta:
        model = Categorias
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la categoria '}),
            'descripcion':
            forms.Textarea(attrs={
                'placeholder': 'ingrese la descripcion de la categoria ',
                'rows': 15,
                'cols': 17}),
        }

    def clean_nombre_categoria(self):
        nombre = self.cleaned_data.get('nombre_categoria')
        print(nombre)
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            print("En el error")
            raise forms.ValidationError(
                'El nombre solo puede contener letras y espacios')
        return nombre


class Entrada_vehiculoForm(forms.ModelForm):

    class Meta:
        model = Entrada_vehiculo
        fields = '__all__'
        widgets = {
            'documento': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el documento'
            }),
            'placa': forms.TextInput(attrs={
                'placeholder': 'Ingrese la placa'
            }),
            'fecha_hora_entrada': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
        }

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        print("DOCUMENTO:", documento)

        if documento is None:
            print("DOCUMENTO VACÍO")
            raise forms.ValidationError(
                'El documento es obligatorio'
            )

        if int(documento) <= 0:
            print(" DOCUMENTO INVÁLIDO")
            raise forms.ValidationError(
                'El documento debe ser mayor que cero'
            )

        print(" DOCUMENTO VALIDO")
        return documento

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')

        if placa:
            placa = placa.upper()

        if not re.match(r'^[A-Z]{3}[0-9]{3}$', placa):
            raise forms.ValidationError(
                'La placa debe tener 3 letras mayúsculas y 3 números '
            )

        return placa


class VentasForm(forms.ModelForm):

    class Meta:
        model = Ventas
        fields = [
            'fecha',
            'documento',
            'cliente',
            'usuario',
            'productos',
            'salida',
            'total',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'total': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el total'
            }),
            'documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el documento'
            }),
            'contrasena': forms.PasswordInput(attrs={
                'placeholder': 'Ingrese la contraseña'
            }),
            'producto': forms.SelectMultiple(attrs={
            }),
        }

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        print("DOCUMENTO:", documento)

        if not documento.isdigit():
            print(" ERROR DOCUMENTO")
            raise forms.ValidationError(
                'El documento solo puede contener números'
            )
        if len(documento) > 10 or len(documento) < 10:
            raise forms.ValidationError(
                "El documento tiene que tener 10 digitos")
        return documento

    def clean_total(self):
        total = self.cleaned_data.get('total')
        print("TOTAL:", total)

        if total is None or total <= 0:
            print(" ERROR TOTAL")
            raise forms.ValidationError(
                'El total debe ser mayor que cero'
            )

        print(" TOTAL OK")
        return total

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        fecha_actual = timezone.now().date()
        print(fecha)
        print(fecha_actual)
        if fecha != fecha_actual:
            raise forms.ValidationError(
                "La fecha tiene que ser la del dia de hoy")
        return fecha


    def clean(self):
        cleaned_data = super().clean()
        productos = cleaned_data.get('productos')

        if productos:
            cleaned_data['total'] = sum(p.precio for p in productos)

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # total solo lectura
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['productos'].choices = [
            (p.id, f"{p.nombre} - ${p.precio}") for p in self.fields['productos'].queryset
        ]


class UsuarioForm(ModelForm):

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'contrasena': forms.PasswordInput(attrs={
                'placeholder': 'Ingrese la contraseña'
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        print("NOMBRE:", nombre)

        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            print(" ERROR NOMBRE")
            raise forms.ValidationError(
                'El nombre solo puede contener letras y espacios'
            )

        return nombre

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        print("CONTRASEÑA:", contrasena)

        if not contrasena:
            raise forms.ValidationError(
                'La contraseña es obligatoria'
            )

        if len(contrasena) < 8:
            print(" CONTRASEÑA CORTA")
            raise forms.ValidationError(
                'La contraseña debe tener al menos 8 caracteres'
            )

        return contrasena

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        print("TELÉFONO:", telefono)

        if not telefono.isdigit():
            print(" ERROR TELÉFONO")
            raise forms.ValidationError(
                'El teléfono solo puede contener números'
            )

        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print("EMAIL:", email)

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            print(" ERROR EMAIL")
            raise forms.ValidationError(
                'Ingrese un correo electrónico válido'
            )

        return email
