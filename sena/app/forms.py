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
        exclude = ['total_a_pagar']
        widgets = {
            'fecha_hora_salida': forms.TimeInput(attrs={
                'type': 'datetime-local'
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
        exist = Categorias.objects.filter(nombre_categoria = nombre).exclude(pk=self.instance.pk).exists()
        if exist:
            raise forms.ValidationError("El nombre ya existe")
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
                'placeholder': 'Ingrese el documento',
                'maxlength': '10'  # Límite visual en el navegador
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

        # NUEVA VALIDACIÓN DE LONGITUD PARA EVITAR NÚMEROS INFINITOS
        documento_str = str(documento)
        if len(documento_str) > 10:
            print(" ERROR: DOCUMENTO DEMASIADO LARGO")
            raise forms.ValidationError(
                'El documento no puede tener más de 10 dígitos'
            )

        if int(documento) <= 0:
            print(" DOCUMENTO INVÁLIDO")
            raise forms.ValidationError(
                'El documento debe ser mayor que cero'
            )

        print(" DOCUMENTO VALIDO")
        return documento

    # NUEVA VALIDACIÓN DE PLACA INCORPORADA
    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        exist = Entrada_vehiculo.objects.filter(placa = placa).exclude(pk=self.instance.pk).exists()
        if exist:
            raise forms.ValidationError("Ya existe esta placa")
        if placa:
            placa = placa.upper().strip()
            if not re.match(r'^[A-Z]{3}[0-9]{3}$', placa):
                raise forms.ValidationError(
                    'La placa debe tener 3 letras y 3 números'
                )
        return placa

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
                'placeholder': 'Ingrese el nombre del producto',
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripción del producto',
                'rows': 5,
                'class': 'form-control'
            }),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio',
                'class': 'form-control',
                'step': '0.01'
            }),
            'existencia': forms.NumberInput(attrs={
                'placeholder': 'Ingrese la cantidad disponible',
                'class': 'form-control'
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio')

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise forms.ValidationError(
                'El nombre debe tener mínimo 3 caracteres')

        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError(
                'El nombre solo puede contener letras y espacios')

        existe = Producto.objects.filter(
            nombre__iexact=nombre
        ).exclude(pk=self.instance.pk).exists()

        if existe:
            raise forms.ValidationError(
                'Ya existe un producto con ese nombre')

        return nombre.title()

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')

        if not descripcion:
            raise forms.ValidationError(
                'La descripción es obligatoria')

        descripcion = descripcion.strip()

        if len(descripcion) < 5:
            raise forms.ValidationError(
                'La descripción debe tener mínimo 5 caracteres')

        if not re.match(r'^[a-zA-Z0-9ÁÉÍÓÚáéíóúÑñ\s.,]+$', descripcion):
            raise forms.ValidationError(
                'La descripción contiene caracteres no permitidos')

        return descripcion

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio is None:
            raise forms.ValidationError('El precio es obligatorio')

        if precio <= 0:
            raise forms.ValidationError(
                'El precio debe ser mayor a 0')

        if precio > 100000000:
            raise forms.ValidationError(
                'El precio es demasiado alto')

        return precio

    def clean_existencia(self):
        existencia = self.cleaned_data.get('existencia')

        if existencia is None:
            raise forms.ValidationError(
                'La existencia es obligatoria')

        if existencia < 0:
            raise forms.ValidationError(
                'La existencia no puede ser negativa')

        if existencia > 100000:
            raise forms.ValidationError(
                'Cantidad demasiado grande')

        return existencia

    def clean(self):
        cleaned_data = super().clean()

        precio = cleaned_data.get('precio')
        existencia = cleaned_data.get('existencia')

        if precio is not None and existencia is not None:
            if precio == 0 and existencia > 0:
                raise forms.ValidationError(
                    'Un producto con existencia no puede tener precio 0')

        return cleaned_data




class VehiculoForm(ModelForm):

    class Meta:
        model = Vehiculo
        fields = '__all__'

        widgets = {

            'tipo_vehiculo': forms.Select(attrs={
                'class': 'form-control'
            }),

            'placa': forms.TextInput(attrs={
                'placeholder': 'Ingrese la placa',
                'class': 'form-control',
                'maxlength': '6'
            }),

            'marca': forms.TextInput(attrs={
                'placeholder': 'Ingrese la marca',
                'class': 'form-control'
            }),

            'modelo': forms.TextInput(attrs={
                'placeholder': 'Ingrese el modelo',
                'class': 'form-control'
            }),

            'kilometraje': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el kilometraje',
                'class': 'form-control'
            }),

            'documento': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    # VALIDACIÓN DE PLACA
    

    def clean_placa(self):

        placa = self.cleaned_data.get('placa')

        if not placa:
            raise forms.ValidationError("La placa es obligatoria")

        placa = placa.upper().strip()

        existe = Vehiculo.objects.filter(
            placa=placa
        ).exclude(pk=self.instance.pk).exists()

        if existe:
            raise forms.ValidationError("La placa ya existe")

        if not re.match(r'^[A-Z]{3}[0-9]{3}$', placa):
            raise forms.ValidationError(
                'La placa debe tener 3 letras mayúsculas y 3 números (Ej: ABC123)'
            )

        return placa


    
    # VALIDACIÓN DE KILOMETRAJE
    

    def clean_kilometraje(self):

        kilometraje = self.cleaned_data.get('kilometraje')
        if kilometraje is None:
            raise forms.ValidationError("El kilometraje es obligatorio")

        if kilometraje < 0:
            raise forms.ValidationError("El kilometraje no puede ser negativo")

        if kilometraje > 1000000:
            raise forms.ValidationError("El kilometraje no es válido")

        return kilometraje


    
    # VALIDACIÓN DE MARCA
    

    def clean_marca(self):

        marca = self.cleaned_data.get('marca')

        if not marca:
            raise forms.ValidationError("La marca es obligatoria")

        if not re.match(r'^[a-zA-Z\s]+$', marca):
            raise forms.ValidationError(
                "La marca solo puede contener letras y espacios"
            )

        return marca.title()


    
    # VALIDACIÓN DE MODELO
    

    def clean_modelo(self):

        modelo = self.cleaned_data.get('modelo')
        if not re.fullmatch(r'^[0-9]+$', str(modelo)):
            raise forms.ValidationError("El kilometraje solo puede contener números")
        if not modelo:
            raise forms.ValidationError("El modelo es obligatorio")

        if len(modelo) > 30:
            raise forms.ValidationError(
                "El modelo no puede tener más de 30 caracteres"
            )

        return modelo


    
    # VALIDACIÓN DE DOCUMENTO
    

    def clean_documento(self):

        documento = self.cleaned_data.get('documento')

        if not documento:
            raise forms.ValidationError("Debe seleccionar un documento")

        return documento


    
    # VALIDACIÓN DE TIPO VEHÍCULO
    

    def clean_tipo_vehiculo(self):

        tipo = self.cleaned_data.get('tipo_vehiculo')

        if not tipo:
            raise forms.ValidationError(
                "Debe seleccionar un tipo de vehículo"
            )

        return tipo



    # VALIDACIÓN GENERAL

    def clean(self):

        cleaned_data = super().clean()

        marca = cleaned_data.get('marca')
        modelo = cleaned_data.get('modelo')

        if marca and modelo:
            if marca.lower() == modelo.lower():
                raise forms.ValidationError(
                    "La marca y el modelo no pueden ser iguales"
                )

        return cleaned_data
    

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
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().date().isoformat(),
                'max': timezone.now().date().isoformat()
            }),
            'total': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el total'
            }),
            'documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el documento'
            }),
            'productos': forms.SelectMultiple(),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        hoy = timezone.now().date()
        if fecha != hoy:
            raise forms.ValidationError('Solo se permite la fecha de hoy')
        return fecha

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        if not documento.isdigit():
            raise forms.ValidationError('El documento solo puede contener números')
        if len(documento) != 10:
            raise forms.ValidationError('El documento debe tener 10 dígitos')

        # Validación de documento único por día
        hoy = timezone.now().date()
        if Ventas.objects.filter(documento=documento, fecha=hoy).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este documento ya tiene una venta registrada hoy')
        return documento

    def clean_productos(self):
        productos = self.cleaned_data.get('productos')
        fecha = self.cleaned_data.get('fecha', timezone.now().date())

        # Validación de productos ya vendidos hoy
        for producto in productos:
            if Ventas.objects.filter(productos=producto, fecha=fecha).exists():
                raise forms.ValidationError(
                    f'El producto "{producto.nombre}" ya ha sido vendido hoy'
                )
        return productos

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is None or total <= 0:
            raise forms.ValidationError('El total debe ser mayor que cero')
        return total

    def clean(self):
        cleaned_data = super().clean()
        productos = cleaned_data.get('productos')
        salida = cleaned_data.get('salida')

        total_productos = sum(p.precio for p in productos) if productos else 0
        total_salida = salida.total_a_pagar if salida else 0

        cleaned_data['total'] = total_productos + total_salida
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['productos'].choices = [
            (p.id, f"{p.nombre} - ${p.precio}") for p in self.fields['productos'].queryset
        ]
        self.fields['salida'].choices = [
            (s.id, f"{s.fecha_hora_salida} - ${s.total_a_pagar}") for s in self.fields['salida'].queryset
        ]

class UsuarioForm(ModelForm):
    confirmar_contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma la contraseña'}),
        label="Confirmar contraseña"
    )

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'rol': forms.Select(),
            'contrasena': forms.PasswordInput(attrs={'placeholder': 'Ingrese la contraseña'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')
        
        # Evitar duplicados
        if Usuario.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError('Ya existe un usuario con este nombre')
        return nombre

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise forms.ValidationError('Ingrese un correo electrónico válido')

        # Evitar duplicados
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo ya está registrado')
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            if not telefono.isdigit():
                raise forms.ValidationError('El teléfono solo puede contener números')
            if len(telefono) > 10:
                raise forms.ValidationError("El número debe tener solo 10 dígitos")

            # Evitar duplicados
            if Usuario.objects.filter(telefono=telefono).exists():
                raise forms.ValidationError('Este número de teléfono ya está registrado')
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contrasena')
        confirm_contrasena = cleaned_data.get('confirmar_contraseña')

        if contraseña and confirm_contrasena:
            if contraseña != confirm_contrasena:
                self.add_error('contrasena', "Las contraseñas no coinciden")
                self.add_error('confirmar_contraseña', "Las contraseñas no coinciden")
            else:
                # Validación de complejidad
                errores = []
                if len(contraseña) < 8:
                    errores.append("Debe tener al menos 8 caracteres")
                if not re.search(r'[A-Z]', contraseña):
                    errores.append("Debe contener al menos una letra mayúscula")
                if not re.search(r'[a-z]', contraseña):
                    errores.append("Debe contener al menos una letra minúscula")
                if not re.search(r'\d', contraseña):
                    errores.append("Debe contener al menos un número")
                if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
                    errores.append("Debe contener al menos un carácter especial (!@#$%^&*...)")
                
                if errores:
                    self.add_error('contrasena', "Contraseña inválida: " + ", ".join(errores))
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contrasena'].widget.attrs['value'] = ''
class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre', 'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'placeholder': 'Ingrese el documento', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese el teléfono', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ingrese la dirección', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese el email', 'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        validar_solo_letras(nombre)
        return nombre

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        exist = Proveedor.objects.filter(documento=documento).exclude(id=self.instance.id).exists()
        if exist:
            raise forms.ValidationError('El documento ya existe para otro proveedor')
        if not documento:
            raise forms.ValidationError('El documento es obligatorio')
        if not documento.isdigit():
            raise forms.ValidationError('El documento solo puede contener números')
        if len(documento) < 7 or len(documento) > 10:
            raise forms.ValidationError('El documento debe tener entre 7 y 10 dígitos')
        return documento

    # --- ESTA ES LA VALIDACIÓN QUE TE FALTABA ---
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            telefono = telefono.strip()
            if not telefono.isdigit():
                raise forms.ValidationError('El teléfono no puede contener letras, solo números.')
            if len(telefono) < 7 or len(telefono) > 10:
                raise forms.ValidationError('El teléfono debe tener entre 7 y 10 dígitos.')
        return telefono
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip()
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                raise forms.ValidationError('Ingrese un correo electrónico válido.')
        return email
class TipoServicioForm(ModelForm):
    class Meta:
        model = tipo_servicio
        fields = ['nombre', 'descripcion', 'categoria', 'estado']

        widgets = {
            'nombre': forms.Select(attrs={'placeholder': 'Nombre del servicio', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción', 'rows': 3, 'class': 'form-control'}),
            'categoria': forms.Select(attrs={'placeholder': 'Categoría', 'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
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


# --- NUEVO FORMULARIO DE COMPRA ---


class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        exclude = ['total']

        # Aquí quitamos el "fk_" de las etiquetas
        labels = {
            'fecha': 'Fecha de Compra',
            'fk_proveedor': 'Proveedor',
            'fk_insumo': 'Insumo',
            'estado': 'Estado del Pedido'
        }
        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Esto pone el CALENDARIO automático
            }),
            'fk_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'fk_insumo': forms.Select(attrs={'class': 'form-control'}),
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
        exist = Cliente.objects.filter(nombre = nombre).exclude(pk=self.instance.pk).exists()
        if exist:
            raise forms.ValidationError("Este nombre ya existe")
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras')

        return nombre

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        exist = Cliente.objects.filter(documento = documento).exclude(pk = self.instance.pk).exists()
        if exist:
            raise forms.ValidationError("Este documento ya esta en uso")
        if not documento.isdigit():
            raise forms.ValidationError(
                'El documento solo puede contener números')

        return documento
    def clean_documento(self):
        documento = self.cleaned_data.get('documento')

        if not documento:
            raise forms.ValidationError('El documento es obligatorio')

        if len(documento) < 8 or len(documento) > 10:
            raise forms.ValidationError(
            'El documento debe tener entre 8 y 10 caracteres')

        if not documento.isdigit():
            raise forms.ValidationError(
            'El documento solo debe contener números')

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
        if titulo:
            titulo = titulo.strip()
            if len(titulo) < 5:
                raise forms.ValidationError(
                    'El título debe tener mínimo 5 caracteres')
        return titulo

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')

        if not mensaje:
            raise forms.ValidationError('El mensaje es obligatorio')

        mensaje = mensaje.strip()

        if len(mensaje) < 10:
            raise forms.ValidationError(
                'El mensaje debe tener mínimo 10 caracteres'
            )

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,]+$', mensaje):
            raise forms.ValidationError(
                'El mensaje solo puede contener letras, números, espacios, punto y coma'
            )

        return mensaje

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < timezone.now().date():
            raise forms.ValidationError('La fecha de la notificación no puede ser anterior a hoy.')
        return fecha
    


class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        exclude = ['subtotal', 'iva', 'total'] 

        labels = {
            'venta': 'Venta Asociada',
            'fecha': 'Fecha de Factura',
        }

        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'venta': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        venta = cleaned_data.get('venta')
        exist = Factura.objects.filter(venta=venta).exclude(id=self.instance.id).exists()
        if exist:
            raise forms.ValidationError('Ya existe una factura para esta venta')
        return cleaned_data
        
