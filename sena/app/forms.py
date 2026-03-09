from django import forms
import re
from datetime import date
from django.utils import timezone
from .models import (
    Proveedor, Producto, Compra, Cliente, Marca, Vehiculo,Factura,
    TipoServicio, OrdenServicio, VentasFactura, Usuario,
    Notificacion, Caja, DetalleOrdenProducto, CompatibilidadProducto
)


# ══════════════════════════════════════════════════════════
#  DICCIONARIO DE INDICATIVOS DE PAÍSES
# ══════════════════════════════════════════════════════════

INDICATIVOS_PAISES = [
    ('',     '-- Indicativo --'),
    ('+57',  '🇨🇴 +57  Colombia'),
    ('+1',   '🇺🇸 +1   Estados Unidos / Canadá'),
    ('+52',  '🇲🇽 +52  México'),
    ('+54',  '🇦🇷 +54  Argentina'),
    ('+55',  '🇧🇷 +55  Brasil'),
    ('+56',  '🇨🇱 +56  Chile'),
    ('+51',  '🇵🇪 +51  Perú'),
    ('+58',  '🇻🇪 +58  Venezuela'),
    ('+593', '🇪🇨 +593 Ecuador'),
    ('+591', '🇧🇴 +591 Bolivia'),
    ('+595', '🇵🇾 +595 Paraguay'),
    ('+598', '🇺🇾 +598 Uruguay'),
    ('+507', '🇵🇦 +507 Panamá'),
    ('+506', '🇨🇷 +506 Costa Rica'),
    ('+503', '🇸🇻 +503 El Salvador'),
    ('+502', '🇬🇹 +502 Guatemala'),
    ('+504', '🇭🇳 +504 Honduras'),
    ('+505', '🇳🇮 +505 Nicaragua'),
    ('+53',  '🇨🇺 +53  Cuba'),
    ('+1809','🇩🇴 +1809 República Dominicana'),
    ('+34',  '🇪🇸 +34  España'),
    ('+44',  '🇬🇧 +44  Reino Unido'),
    ('+33',  '🇫🇷 +33  Francia'),
    ('+49',  '🇩🇪 +49  Alemania'),
    ('+39',  '🇮🇹 +39  Italia'),
    ('+351', '🇵🇹 +351 Portugal'),
    ('+7',   '🇷🇺 +7   Rusia'),
    ('+86',  '🇨🇳 +86  China'),
    ('+81',  '🇯🇵 +81  Japón'),
    ('+82',  '🇰🇷 +82  Corea del Sur'),
    ('+91',  '🇮🇳 +91  India'),
    ('+61',  '🇦🇺 +61  Australia'),
    ('+27',  '🇿🇦 +27  Sudáfrica'),
    ('+20',  '🇪🇬 +20  Egipto'),
    ('+212', '🇲🇦 +212 Marruecos'),
    ('+971', '🇦🇪 +971 Emiratos Árabes'),
    ('+966', '🇸🇦 +966 Arabia Saudita'),
]

def val_telefono_internacional(indicativo, numero, campo):
    if not indicativo:
        raise forms.ValidationError(f"'{campo}': seleccione el indicativo del país.")
    numero_limpio = str(numero).strip()
    if not numero_limpio.isdigit():
        raise forms.ValidationError(f"'{campo}' solo permite números, sin espacios, guiones ni símbolos.")
    if not (6 <= len(numero_limpio) <= 15):
        raise forms.ValidationError(f"'{campo}' debe tener entre 6 y 15 dígitos.")
    return f"{indicativo}{numero_limpio}"


# ══════════════════════════════════════════════════════════
#  UTILIDADES COMPARTIDAS
# ══════════════════════════════════════════════════════════

def val_solo_letras(valor, campo):
    if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', str(valor).strip()):
        raise forms.ValidationError(f"'{campo}' solo permite letras y espacios, sin números ni símbolos.")
    return valor.strip()

def val_solo_numeros(valor, campo):
    limpio = str(valor).strip()
    if not limpio.isdigit():
        raise forms.ValidationError(f"'{campo}' solo permite números, sin letras ni símbolos.")
    return limpio

def val_placa_colombiana(valor):
    placa = str(valor).strip().upper().replace(" ", "")
    if not (re.match(r'^[A-Z]{3}[0-9]{3}$', placa) or re.match(r'^[A-Z]{3}[0-9]{2}[A-Z]{1}$', placa)):
        raise forms.ValidationError("Placa inválida. Use el formato ABC123 (carro) o ABC12D (moto).")
    numeros = re.findall(r'[0-9]+', placa)
    if numeros and numeros[0] == '000':
        raise forms.ValidationError("La placa no puede tener '000' como dígitos. Ej válido: ABC123.")
    return placa

def val_no_negativo(valor, campo):
    if valor < 0:
        raise forms.ValidationError(f"'{campo}' no puede ser un valor negativo.")
    return valor

def val_positivo(valor, campo):
    if valor <= 0:
        raise forms.ValidationError(f"'{campo}' debe ser mayor que 0.")
    return valor

def val_email(valor, campo):
    if not re.match(r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$', str(valor).strip()):
        raise forms.ValidationError(f"'{campo}' no tiene un formato de correo válido. Ej: correo@dominio.com")
    return valor.strip().lower()

def val_telefono_colombiano(valor, campo):
    limpio = str(valor).strip()
    if not limpio.isdigit():
        raise forms.ValidationError(f"'{campo}' solo permite números, sin espacios, guiones ni símbolos.")
    if len(limpio) == 10:
        if limpio.startswith('3'):
            return limpio
        elif limpio.startswith('60') or limpio.startswith('61'):
            return limpio
        else:
            raise forms.ValidationError(
                f"'{campo}': celular debe empezar por 3 (ej: 3107928076) "
                f"o fijo con indicativo por 60/61 (ej: 6012345678)."
            )
    elif len(limpio) == 7:
        return limpio
    else:
        raise forms.ValidationError(
            f"'{campo}' inválido. Use 10 dígitos para celular (ej: 3107928076) "
            f"o 7 dígitos para fijo local (ej: 2345678). "
            f"Recibido: {len(limpio)} dígitos."
        )

def val_documento_colombiano(valor, campo, tipo_doc=None):
    limpio = str(valor).strip()
    if tipo_doc == 'NIT':
        if not limpio.isdigit() or not (9 <= len(limpio) <= 10):
            raise forms.ValidationError(f"'{campo}': NIT debe tener 9 o 10 dígitos.")
    elif tipo_doc == 'CC':
        if not limpio.isdigit() or not (8 <= len(limpio) <= 14):
            raise forms.ValidationError(f"'{campo}': Cédula debe tener entre 8 y 14 dígitos.")
    elif tipo_doc == 'CE':
        if not limpio.isdigit() or not (8 <= len(limpio) <= 14):
            raise forms.ValidationError(f"'{campo}': Cédula de extranjería debe tener entre 8 y 14 dígitos.")
    elif tipo_doc == 'PAS':
        if not re.match(r'^[A-Z0-9]{5,12}$', limpio.upper()):
            raise forms.ValidationError(f"'{campo}': Pasaporte debe tener entre 5 y 12 caracteres alfanuméricos.")
    else:
        if not limpio.isdigit():
            raise forms.ValidationError(f"'{campo}' solo permite números.")
        if not (8 <= len(limpio) <= 14):
            raise forms.ValidationError(f"'{campo}' debe tener entre 8 y 14 dígitos.")
    return limpio


# ══════════════════════════════════════════════════════════
#  USUARIO
# ══════════════════════════════════════════════════════════

class UsuarioForm(forms.ModelForm):

    indicativo_telefono = forms.ChoiceField(
        choices=INDICATIVOS_PAISES,
        required=False,
        label="Indicativo",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    numero_telefono = forms.CharField(
        max_length=15,
        required=False,
        label="Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3107928076'}),
    )

    class Meta:
        model = Usuario
        exclude = ['fecha_registro']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.telefono:
            tel = self.instance.telefono
            for code, _ in INDICATIVOS_PAISES:
                if code and tel.startswith(code):
                    self.fields['indicativo_telefono'].initial = code
                    self.fields['numero_telefono'].initial = tel[len(code):]
                    break
            else:
                self.fields['indicativo_telefono'].initial = '+57'
                self.fields['numero_telefono'].initial = tel

    def clean_nombres(self):
        nombres = val_solo_letras(self.cleaned_data['nombres'], "Nombres")
        if len(nombres) < 2:
            raise forms.ValidationError("'Nombres' debe tener al menos 2 caracteres.")
        return nombres

    def clean_apellidos(self):
        apellidos = val_solo_letras(self.cleaned_data['apellidos'], "Apellidos")
        if len(apellidos) < 2:
            raise forms.ValidationError("'Apellidos' debe tener al menos 2 caracteres.")
        return apellidos

    def clean_cedula(self):
        cedula = val_solo_numeros(self.cleaned_data['cedula'], "Cédula")
        if not (8 <= len(cedula) <= 14):
            raise forms.ValidationError("La cédula debe tener entre 8 y 14 dígitos.")
        qs = Usuario.objects.filter(cedula=cedula)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario registrado con esta cédula.")
        return cedula

    def clean_telefono(self):
        return self.cleaned_data.get('telefono')

    def clean_correo(self):
        correo = val_email(self.cleaned_data['correo'], "Correo")
        qs = Usuario.objects.filter(correo=correo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo.")
        return correo

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe tener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("La contraseña debe tener al menos una letra minúscula.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("La contraseña debe tener al menos un número.")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?]', password):
            raise forms.ValidationError("La contraseña debe tener al menos un carácter especial. Ej: !@#$%&*")
        return password

    def clean(self):
        cleaned = super().clean()
        indicativo = cleaned.get('indicativo_telefono', '')
        numero = cleaned.get('numero_telefono', '')
        if indicativo or numero:
            telefono_completo = val_telefono_internacional(indicativo, numero, "Teléfono")
            cleaned['telefono'] = telefono_completo
        password = cleaned.get('password')
        confirmacion = cleaned.get('password_confirmacion')
        if password and confirmacion and password != confirmacion:
            self.add_error('password_confirmacion', "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            instance.telefono = telefono
        if commit:
            instance.save()
        return instance


# ══════════════════════════════════════════════════════════
#  PROVEEDOR
# ══════════════════════════════════════════════════════════

class ProveedorForm(forms.ModelForm):

    indicativo_telefono = forms.ChoiceField(
        choices=INDICATIVOS_PAISES,
        required=True,
        label="Indicativo",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    numero_telefono = forms.CharField(
        max_length=15,
        required=True,
        label="Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3107928076'}),
    )

    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.telefono:
            tel = self.instance.telefono
            for code, _ in INDICATIVOS_PAISES:
                if code and tel.startswith(code):
                    self.fields['indicativo_telefono'].initial = code
                    self.fields['numero_telefono'].initial = tel[len(code):]
                    break
            else:
                self.fields['indicativo_telefono'].initial = '+57'
                self.fields['numero_telefono'].initial = tel

    def clean_nombre(self):
        nombre = val_solo_letras(self.cleaned_data['nombre'], "Nombre del proveedor")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del proveedor debe tener al menos 3 caracteres.")
        return nombre

    def clean_nit(self):
        nit = val_solo_numeros(self.cleaned_data['nit'], "NIT")
        if not (9 <= len(nit) <= 10):
            raise forms.ValidationError("El NIT debe tener 9 o 10 dígitos.")
        if int(nit) <= 0:
            raise forms.ValidationError("El NIT debe ser mayor que 0.")
        if len(set(nit)) == 1:
            raise forms.ValidationError("El NIT no puede tener todos los dígitos iguales. Ej: 111111111 no es válido.")
        qs = Proveedor.objects.filter(nit=nit)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un proveedor registrado con este NIT.")
        return nit

    def clean_telefono(self):
        return self.cleaned_data.get('telefono')

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if direccion and len(direccion) < 5:
            raise forms.ValidationError("La dirección es demasiado corta (mínimo 5 caracteres).")
        return direccion

    def clean(self):
        cleaned = super().clean()
        indicativo = cleaned.get('indicativo_telefono', '')
        numero = cleaned.get('numero_telefono', '')
        if indicativo or numero:
            telefono_completo = val_telefono_internacional(indicativo, numero, "Teléfono")
            cleaned['telefono'] = telefono_completo
            qs = Proveedor.objects.filter(telefono=telefono_completo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('numero_telefono', "Ya existe un proveedor registrado con este teléfono.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            instance.telefono = telefono
        if commit:
            instance.save()
        return instance


# ══════════════════════════════════════════════════════════
#  MARCA
# ══════════════════════════════════════════════════════════

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9\s\-]+$', nombre):
            raise forms.ValidationError("El nombre solo permite letras, números, espacios y guiones.")
        if nombre and nombre[0].isdigit():
            raise forms.ValidationError("El nombre de la marca no puede iniciar con un número.")
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        qs = Marca.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Esta marca ya existe en el sistema.")
        return nombre

    def clean_pais_origen(self):
        pais = self.cleaned_data.get('pais_origen', '')
        if pais:
            pais = pais.strip()
            if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', pais):
                raise forms.ValidationError("El país solo permite letras y espacios, sin números ni símbolos.")
            if len(pais) < 3:
                raise forms.ValidationError("El nombre del país debe tener al menos 3 caracteres.")
        return pais

    def clean_descripcion(self):
        desc = self.cleaned_data.get('descripcion', '').strip()
        if desc:
            if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9\s\.,\-\(\)]+$', desc):
                raise forms.ValidationError("La descripción no permite caracteres especiales.")
            if len(desc) < 5:
                raise forms.ValidationError("La descripción es demasiado corta (mínimo 5 caracteres).")
            if len(desc) > 200:
                raise forms.ValidationError("La descripción no puede superar 200 caracteres.")
        return desc

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo and hasattr(logo, 'name'):
            ext = logo.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError("Solo se permiten imágenes JPG, PNG o WEBP.")
            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("La imagen no puede superar los 2 MB.")
        return logo


# ══════════════════════════════════════════════════════════
#  PRODUCTO
# ══════════════════════════════════════════════════════════

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def clean_codigo(self):
        codigo = val_solo_numeros(self.cleaned_data['codigo'], "Código")
        if len(codigo) < 3:
            raise forms.ValidationError("El código debe tener al menos 3 dígitos.")
        qs = Producto.objects.filter(codigo=codigo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con este código.")
        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del producto debe tener al menos 3 caracteres.")
        qs = Producto.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con este nombre.")
        return nombre

    def clean_precio(self):
        precio = val_positivo(self.cleaned_data['precio'], "Precio")
        if precio > 99999999:
            raise forms.ValidationError("El precio ingresado es demasiado alto.")
        return precio

    def clean_stock(self):
        return val_no_negativo(self.cleaned_data['stock'], "Stock")

    def clean_stock_minimo(self):
        return val_no_negativo(self.cleaned_data['stock_minimo'], "Stock mínimo")

    def clean(self):
        cleaned = super().clean()
        stock = cleaned.get('stock')
        stock_min = cleaned.get('stock_minimo')
        if stock is not None and stock_min is not None:
            if stock_min > stock:
                self.add_error('stock_minimo', "El stock mínimo no puede ser mayor al stock actual.")
        return cleaned


# ══════════════════════════════════════════════════════════
#  COMPRA
# ══════════════════════════════════════════════════════════

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'

    def clean_cantidad(self):
        cantidad = val_positivo(self.cleaned_data['cantidad'], "Cantidad")
        if cantidad > 10000:
            raise forms.ValidationError("La cantidad no puede superar 10.000 unidades por compra.")
        return cantidad

    def clean_num_factura_proveedor(self):
        nf = self.cleaned_data['num_factura_proveedor'].strip()
        if not nf:
            raise forms.ValidationError("El número de factura es obligatorio.")
        if len(nf) < 3:
            raise forms.ValidationError("El número de factura debe tener al menos 3 caracteres.")
        qs = Compra.objects.filter(num_factura_proveedor=nf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una compra registrada con este número de factura.")
        return nf

    def clean_total_pagado(self):
        total = val_no_negativo(self.cleaned_data['total_pagado'], "Total pagado")
        if total > 999999999:
            raise forms.ValidationError("El total pagado es demasiado alto. Verifique el valor.")
        return total

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            hoy = timezone.now().date()
            fecha_date = fecha.date() if hasattr(fecha, 'date') else fecha
            if fecha_date != hoy:
                raise forms.ValidationError(
                    f"La fecha de compra debe ser el día de hoy ({hoy.strftime('%d/%m/%Y')}). "
                    "No se permiten fechas pasadas ni futuras."
                )
        return fecha


# ══════════════════════════════════════════════════════════
#  CLIENTE
# ══════════════════════════════════════════════════════════

class ClienteForm(forms.ModelForm):

    indicativo_telefono = forms.ChoiceField(
        choices=INDICATIVOS_PAISES,
        required=True,
        label="Indicativo",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    numero_telefono = forms.CharField(
        max_length=15,
        required=True,
        label="Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3107928076'}),
    )

    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.telefono:
            tel = self.instance.telefono
            for code, _ in INDICATIVOS_PAISES:
                if code and tel.startswith(code):
                    self.fields['indicativo_telefono'].initial = code
                    self.fields['numero_telefono'].initial = tel[len(code):]
                    break
            else:
                self.fields['indicativo_telefono'].initial = '+57'
                self.fields['numero_telefono'].initial = tel

    def clean_nombre(self):
        nombre = val_solo_letras(self.cleaned_data['nombre'], "Nombre del cliente")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_numero_documento(self):
        tipo_doc = self.cleaned_data.get('tipo_documento', 'CC')
        doc = self.cleaned_data['numero_documento'].strip()
        doc = val_documento_colombiano(doc, "Número de documento", tipo_doc)
        qs = Cliente.objects.filter(numero_documento=doc)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un cliente registrado con este número de documento.")
        return doc

    def clean_telefono(self):
        return self.cleaned_data.get('telefono')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = val_email(email, "Email")
            qs = Cliente.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe un cliente registrado con este email.")
        return email

    def clean(self):
        cleaned = super().clean()
        indicativo = cleaned.get('indicativo_telefono', '')
        numero = cleaned.get('numero_telefono', '')
        if indicativo or numero:
            telefono_completo = val_telefono_internacional(indicativo, numero, "Teléfono")
            cleaned['telefono'] = telefono_completo
            qs = Cliente.objects.filter(telefono=telefono_completo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('numero_telefono', "Ya existe un cliente registrado con este teléfono.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            instance.telefono = telefono
        if commit:
            instance.save()
        return instance


# ══════════════════════════════════════════════════════════
#  VEHÍCULO
# ══════════════════════════════════════════════════════════

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

    def clean_placa(self):
        placa = val_placa_colombiana(self.cleaned_data['placa'])
        qs = Vehiculo.objects.filter(placa=placa)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"Ya existe un vehículo registrado con la placa '{placa}'.")
        return placa

    def clean_modelo(self):
        modelo = self.cleaned_data['modelo'].strip()
        if not re.match(r'^\d{4}$', modelo):
            raise forms.ValidationError("El año debe tener exactamente 4 dígitos. Ej: 2019")
        anio = int(modelo)
        anio_actual = date.today().year
        if anio < 1900 or anio > anio_actual:
            raise forms.ValidationError(f"El año debe estar entre 1900 y {anio_actual}.")
        return modelo


# ══════════════════════════════════════════════════════════
#  TIPO DE SERVICIO
# ══════════════════════════════════════════════════════════

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del servicio debe tener al menos 3 caracteres.")
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9\s\-\/]+$', nombre):
            raise forms.ValidationError("El nombre solo permite letras, números, espacios, guiones y barras.")
        qs = TipoServicio.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un tipo de servicio con este nombre.")
        return nombre

    def clean_precio_mano_obra(self):
        precio = val_positivo(self.cleaned_data['precio_mano_obra'], "Precio de mano de obra")
        if precio > 99999999:
            raise forms.ValidationError("El precio de mano de obra es demasiado alto.")
        return precio


# ══════════════════════════════════════════════════════════
#  ORDEN DE SERVICIO
# ══════════════════════════════════════════════════════════

class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = '__all__'

    def clean_km_actual(self):
        km = self.cleaned_data.get('km_actual')

        if km is None:
            raise forms.ValidationError("El kilometraje es obligatorio.")
        if not isinstance(km, int):
            raise forms.ValidationError("El kilometraje debe ser un número entero, sin decimales.")
        if km < 0:
            raise forms.ValidationError("El kilometraje no puede ser negativo.")
        if km == 0:
            raise forms.ValidationError("El kilometraje debe ser mayor que 0. Ingrese el km actual del vehículo.")
        if km > 1000000:
            raise forms.ValidationError("El kilometraje ingresado es demasiado alto (máx. 1.000.000 km).")

        return km

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        if not fecha:
            return timezone.now()

        # No puede ser futura
        if fecha > timezone.now():
            raise forms.ValidationError("La fecha de la orden no puede ser una fecha futura.")

        # No puede ser anterior a 30 días
        limite = timezone.now() - timezone.timedelta(days=30)
        if fecha < limite:
            raise forms.ValidationError(
                "La fecha de la orden no puede ser anterior a 30 días. "
                "Si necesita registrar una orden antigua, contacte al administrador."
            )

        return fecha

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        estados_validos = [e[0] for e in OrdenServicio.ESTADOS]
        if estado not in estados_validos:
            raise forms.ValidationError(
                f"Estado no válido. Opciones permitidas: {', '.join(estados_validos)}."
            )
        return estado

    def clean(self):
        cleaned = super().clean()
        vehiculo = cleaned.get('vehiculo')
        estado   = cleaned.get('estado')

        # No se puede crear una orden nueva directamente como Terminado
        if not self.instance.pk and estado == 'Terminado':
            self.add_error('estado',
                "No puede crear una orden con estado 'Terminado'. "
                "Inicie con 'Pendiente' o 'En Proceso'.")

        # No puede haber dos órdenes activas para el mismo vehículo
        if vehiculo and not self.instance.pk:
            orden_activa = OrdenServicio.objects.filter(
                vehiculo=vehiculo,
                estado__in=['Pendiente', 'En Proceso']
            ).exists()
            if orden_activa:
                self.add_error('vehiculo',
                    f"El vehículo con placa '{vehiculo.placa}' ya tiene una orden activa "
                    "(Pendiente o En Proceso). Finalícela antes de crear una nueva.")

        return cleaned


# ══════════════════════════════════════════════════════════
#  DETALLE ORDEN PRODUCTO
# ══════════════════════════════════════════════════════════

class DetalleOrdenProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenProducto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0, estado=True)

    def clean_cantidad(self):
        cantidad = val_positivo(self.cleaned_data['cantidad'], "Cantidad")
        if cantidad > 1000:
            raise forms.ValidationError("La cantidad no puede superar 1.000 unidades por detalle.")
        return cantidad

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        cantidad = cleaned.get('cantidad')
        if producto and cantidad:
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f"Stock insuficiente para '{producto.nombre}'. "
                    f"Disponible: {producto.stock}, solicitado: {cantidad}."
                )
        return cleaned


# ══════════════════════════════════════════════════════════
#  VENTAS / FACTURA
# ══════════════════════════════════════════════════════════

class VentasFacturaForm(forms.ModelForm):
    class Meta:
        model = VentasFactura
        fields = '__all__'

    def clean_numero_factura(self):
        nf = self.cleaned_data['numero_factura'].strip()
        if not nf:
            raise forms.ValidationError("El número de factura es obligatorio.")
        if len(nf) < 3:
            raise forms.ValidationError("El número de factura debe tener al menos 3 caracteres.")
        qs = VentasFactura.objects.filter(numero_factura=nf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una factura de venta con este número.")
        return nf

    def clean_total(self):
        total = val_no_negativo(self.cleaned_data['total'], "Total de factura")
        if total > 999999999:
            raise forms.ValidationError("El total de la factura es demasiado alto. Verifique el valor.")
        return total


# ══════════════════════════════════════════════════════════
#  CAJA
# ══════════════════════════════════════════════════════════

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = '__all__'

    def clean_monto(self):
        monto = val_positivo(self.cleaned_data['monto'], "Monto")
        if monto > 999999999:
            raise forms.ValidationError("El monto es demasiado alto. Verifique el valor.")
        return monto

    def clean_descripcion(self):
        desc = self.cleaned_data['descripcion'].strip()
        if len(desc) < 5:
            raise forms.ValidationError("La descripción es demasiado corta (mínimo 5 caracteres).")
        if len(desc) > 255:
            raise forms.ValidationError("La descripción no puede superar 255 caracteres.")
        return desc

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > timezone.now():
            raise forms.ValidationError("La fecha del movimiento no puede ser una fecha futura.")
        return fecha

    def clean_comprobante(self):
        archivo = self.cleaned_data.get('comprobante')
        if archivo:
            ext = archivo.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Solo se permiten archivos PDF, JPG o PNG.")
            if archivo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("El archivo no puede superar los 5 MB.")
        return archivo

    def clean_observaciones(self):
        obs = self.cleaned_data.get('observaciones', '').strip()
        if obs and len(obs) < 10:
            raise forms.ValidationError("Las observaciones son demasiado cortas (mínimo 10 caracteres).")
        return obs or None


# ══════════════════════════════════════════════════════════
#  NOTIFICACIÓN
# ══════════════════════════════════════════════════════════

class NotificacionForm(forms.ModelForm):
    TIPOS_NOTIFICACION = [
        ('',              '-- Seleccione un tipo --'),
        ('Alerta',        'Alerta'),
        ('Recordatorio',  'Recordatorio'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Urgente',       'Urgente'),
        ('Informacion',   'Información'),
    ]

    tipo = forms.ChoiceField(
        choices=TIPOS_NOTIFICACION,
        label="Tipo de Notificación",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Notificacion
        fields = '__all__'

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if not tipo:
            raise forms.ValidationError("Seleccione un tipo de notificación.")
        tipos_validos = [t[0] for t in self.TIPOS_NOTIFICACION if t[0]]
        if tipo not in tipos_validos:
            raise forms.ValidationError("Tipo de notificación no válido.")
        return tipo

    def clean_mensaje(self):
        msg = self.cleaned_data['mensaje'].strip()
        if len(msg) < 10:
            raise forms.ValidationError("El mensaje es demasiado corto (mínimo 10 caracteres).")
        if len(msg) > 500:
            raise forms.ValidationError("El mensaje no puede superar 500 caracteres.")
        return msg


# ══════════════════════════════════════════════════════════
#  COMPATIBILIDAD PRODUCTO
# ══════════════════════════════════════════════════════════

class CompatibilidadProductoForm(forms.ModelForm):
    class Meta:
        model = CompatibilidadProducto
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        marca_vehiculo = cleaned.get('marca_vehiculo')
        if producto and marca_vehiculo:
            qs = CompatibilidadProducto.objects.filter(
                producto=producto,
                marca_vehiculo=marca_vehiculo
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    f"Ya existe la compatibilidad entre '{producto.nombre}' "
                    f"y la marca '{marca_vehiculo.nombre}'."
                )
        return cleaned
    
   

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            'tipo', 'numero_factura',
            'orden_servicio', 'producto', 'cantidad',
        ]
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_tipo',
            }),
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: FAC-0001',
            }),
            'orden_servicio': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_orden_servicio',
            }),
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_producto',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'id': 'id_cantidad',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo órdenes terminadas o en proceso
        self.fields['orden_servicio'].queryset = OrdenServicio.objects.filter(
            estado__in=['En Proceso', 'Terminado']
        ).select_related('vehiculo', 'servicio')
        self.fields['orden_servicio'].empty_label = "-- Seleccione una Orden --"
        self.fields['orden_servicio'].required = False

        self.fields['producto'].queryset = Producto.objects.filter(estado=True, stock__gt=0)
        self.fields['producto'].empty_label = "-- Seleccione un Producto --"
        self.fields['producto'].required = False

        self.fields['cantidad'].required = False

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        orden = cleaned.get('orden_servicio')
        producto = cleaned.get('producto')
        cantidad = cleaned.get('cantidad')

        if tipo == 'SERVICIO':
            if not orden:
                self.add_error('orden_servicio', "Seleccione una Orden de Servicio.")
        elif tipo == 'PRODUCTO':
            if not producto:
                self.add_error('producto', "Seleccione un Producto.")
            if not cantidad or cantidad < 1:
                self.add_error('cantidad', "Ingrese una cantidad válida (mínimo 1).")
            elif producto and cantidad > producto.stock:
                self.add_error('cantidad',
                    f"Stock insuficiente. Disponible: {producto.stock}, solicitado: {cantidad}."
                )

        nf = cleaned.get('numero_factura', '').strip()
        if not nf:
            self.add_error('numero_factura', "El número de factura es obligatorio.")
        elif len(nf) < 3:
            self.add_error('numero_factura', "El número de factura debe tener al menos 3 caracteres.")
        else:
            qs = Factura.objects.filter(numero_factura=nf)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('numero_factura', "Ya existe una factura con este número.")

        return cleaned