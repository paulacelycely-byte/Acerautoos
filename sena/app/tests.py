from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))  
from sena.asgi import * #importan la ruta del proyecto
from app.models import *  #importan los modelos  
# Create your tests here.

#insertar
'''
t = Categoria(nombre="estufa", descripcion="dispositivos electronicos")
t.save()
t = Categoria(nombre="ducha", descripcion="dispositivos electronicos")
t.save()

t = Categoria(nombre="nevera", descripcion="dispositivos electronicos")
t.save()  
print("categoria guardada")
'''

# listar
#query = Categoria.objects.all()
#print(query)

# editar
#try:
#    t = Categoria.objects.get(id=1)
#    print(t.nombre)
#    t.nombre = "Lavadora"
#    t.save()
#    print("Categoria actualizada")
#except Exception as e:
#    print(e)

# eliminar
'''
t = Categoria.objects.get(id=1)
t.delete()
print(t)
'''

#listar con filtros

'''
obj = Categoria.objects.filter(nombre__contains="electro")
print(obj)
'''
'''
for i in Categoria.objects.filter(nombre__contains="la"):
    print(i.id, i.nombre, )
'''
#guardar dentro de lista de fonma masiva
'''
data = ['electrodomesticos', 'muebles', 'tecnologia', 'ropa']

for i in data: 
    cat= Categoria.objects.create(
        nombre=i,
        descripcion=f'descripcion de {i}'
        
    )
    cat.save()
    print(f'categoria {cat.nombre} creada con exito')
'''
    
    
    

