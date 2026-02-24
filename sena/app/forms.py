import re
from django.forms import ModelForm
from app.models import Categorias
from app.models import Entrada_vehiculo
from django import forms  
from app.models import Ventas
from app.models import Usuario

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
        
    def clean_nombre_categoria(self):
        nombre= self.cleaned_data.get('nombre_categoria')
        print(nombre)
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            print("En el error")
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')
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
        print("PLACA:", placa)

        if not re.match(r'^[A-Za-z0-9\-]+$', placa):
            print(" ERROR PLACA")
            raise forms.ValidationError(
                'La placa solo puede contener letras y números'
            )

        print(" PLACA VALIDA")
        return placa


    
class VentasForm(forms.ModelForm):

    class Meta:
        model = Ventas
        fields = '__all__'
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
        }

    
    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        print("DOCUMENTO:", documento)

        if not documento.isdigit():
            print(" ERROR DOCUMENTO")
            raise forms.ValidationError(
                'El documento solo puede contener números'
            )

        print(" DOCUMENTO OK")
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
