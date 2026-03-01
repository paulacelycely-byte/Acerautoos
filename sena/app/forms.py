from django import forms
import re
from django.forms import ModelForm
from app.models import *
from django.utils import timezone

# --- FUNCIONES DE VALIDACIÓN ---


def validar_solo_letras(valor):
    if any(char.isdigit() for char in valor):
        raise forms.ValidationError("Este campo no puede contener números.")
    if valor and valor.strip() == "0":
        raise forms.ValidationError("El valor no puede ser solo '0'.")

# --- FORMULARIOS ---


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
            raise forms.ValidationError(
                'La fecha y hora de salida es requerida.')
        return fecha_hora_salida

    def clean_total_a_pagar(self):
        total_a_pagar = self.cleaned_data.get('total_a_pagar')
        if total_a_pagar <= 0:
            raise forms.ValidationError(
                'El total a pagar debe ser un número positivo.')
        return total_a_pagar

    def clean_entrada_id(self):
        entrada = self.cleaned_data.get('entrada_id')
        if not entrada:
            raise forms.ValidationError('La entrada de vehículo es requerida.')
        return entrada


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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError(
                'El nombre solo puede contener letras y espacios')

        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')

        if len(descripcion) > 100:
            raise forms.ValidationError(
                'La descripcion no puede exceder los 100 caracteres')

        # VALIDACION AGREGADA
        if not re.match(r'^[a-zA-Z0-9\s.,]+$', descripcion):
            raise forms.ValidationError(
                'La descripcion contiene caracteres no permitidos')

        return descripcion


class ProductosForm(ModelForm):
    class Meta:
        model = Producto
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
            raise forms.ValidationError(
                'El nombre debe tener mínimo 3 caracteres')

        # AGREGADO: solo letras
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError(
                'El nombre solo puede contener letras y espacios')

        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')

        if len(descripcion) < 5:
            raise forms.ValidationError(
                'La descripcion debe tener mínimo 5 caracteres')

        # AGREGADO
        if not re.match(r'^[a-zA-Z0-9\s.,]+$', descripcion):
            raise forms.ValidationError(
                'La descripcion contiene caracteres no permitidos')

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
        fields = ['nombre', 'descripcion', 'categoria',
                  'hora_entrada_estimada', 'hora_salida_estimada', 'estado']

        widgets = {
            'nombre': forms.Select(attrs={'placeholder': 'Nombre del servicio', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción', 'rows': 3, 'class': 'form-control'}),
            'categoria': forms.Select(attrs={'placeholder': 'Categoría', 'class': 'form-control'}),
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
                self.add_error(
                    'hora_salida_estimada', "La hora de salida debe ser posterior a la de entrada.")
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
                'type': 'date'  # Esto pone el CALENDARIO automático
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
            raise forms.ValidationError(
                "El precio total no puede ser negativo.")
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
            raise forms.ValidationError(
                'El campo nombre solo puede contener letras y espacios.')
        return nombre

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError(
                'La cantidad debe ser un número positivo.')
        return cantidad

    def clean_precio_unitario(self):
        precio_unitario = self.cleaned_data.get('precio_unitario')
        if precio_unitario <= 0:
            raise forms.ValidationError(
                'El precio unitario debe ser un número positivo.')
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
            raise forms.ValidationError(
                'La descripción debe tener al menos 10 caracteres.')
        return descripcion

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError(
                'El precio debe ser un número positivo.')
        return precio

    def clean_kilometraje(self):
        kilometraje = self.cleaned_data.get('kilometraje')

        if kilometraje < 0:
            raise forms.ValidationError('El kilometraje no puede ser negativo')

        return kilometraje

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')

        if not documento.isdigit():
            raise forms.ValidationError(
                'El documento solo puede contener números')

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
            raise forms.ValidationError(
                'El documento solo puede contener números')

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
            raise forms.ValidationError(
                'El titulo debe tener mínimo 5 caracteres')

        return titulo

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')

        if len(mensaje) < 10:
            raise forms.ValidationError(
                'El mensaje debe tener mínimo 10 caracteres')

        return mensaje
