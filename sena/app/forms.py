from dataclasses import fields
from django.forms import ModelForm
from app.models import Categoria
from django import forms  

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
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