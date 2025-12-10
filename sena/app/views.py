from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from  app.models import *


# Create your views here.
#diccionario
producto ={
    'nombre': 'camisa',
    'precio': 150,
}

def vista1(request):
    producto = Categoria.objects.all()
    return render(request, "body.html", {'producto': producto})

def vista2(request):
    producto = Categoria.objects.all()
    return render(request, "index2.html", {'producto':producto})

def vista3(request):
    data = {
        'mensaje': 'hola aguanta se va a poner peor',
        'estado': 'exito',
        
    }
    return JsonResponse(data)
