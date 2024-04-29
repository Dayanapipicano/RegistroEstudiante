import json
from django.shortcuts import render
from apps.usuarios.models import Estudiante
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.usuarios.models import Estado
from django.shortcuts import  redirect
from django.views.generic import  ListView
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
#VISTA PRINCIPAL
class principal(ListView):
    """
    funcion de la vista principal
    """
    model=Estudiante
    template_name='registro.html'
    context_object_name='est'
    queryset=Estudiante.objects.all()
    
    
#REGISTRO DE ESTUDIANTE

def registrar_estudiante(request):
    
    estados = Estado.objects.all()  # Obtener todos los estados disponibles

    if request.method == 'POST':
        nombre = request.POST.get('knombre')
        apellido = request.POST.get('kapellido')
        edad = request.POST.get('kedad')
        correo = request.POST.get('kcorreo')
        estado = request.POST.get('kestado')

        estado = Estado.objects.get(id=estado) 
        Estudiante.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            correo=correo,
            estado=estado,
        )
        
        return redirect('listar_estudiante')
    else:
        return render(request, 'registro.html', {'estados': estados})

#EDITAR ESTUDIANTE 

def editar_estudiante(request, id):
    
    # Obtener todos los estados
    estados = Estado.objects.all()
    # Obtener el estudiante por su ID
    estudiante = Estudiante.objects.get(id=id)
    
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por POST
        nombre = request.POST.get('knombre')
        apellido = request.POST.get('kapellido')
        edad = request.POST.get('kedad')
        correo = request.POST.get('kcorreo')
        estado = request.POST.get('kestado')
        
        # Actualizar los datos del estudiante
        estudiante.nombre = nombre
        estudiante.apellido = apellido
        estudiante.edad = edad
        estudiante.correo = correo
        estudiante.estado_id = estado
        estudiante.save()  
    
        return redirect('listar_estudiante')
    
    # Renderizar el formulario de edición con los datos del estudiante y la lista de estados
    return render(request, 'editar_estudiante.html', {'estudiante': estudiante, 'estados': estados})


#LISTAR ESTUDIANTE -PAGINACION
def paginacion(request):
    estudiantes = Estudiante.objects.all()
    
    # Obtener todos los estados disponibles
    estados = Estado.objects.all()

    paginacion = Paginator(estudiantes, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginacion.get_page(page_number)
    
    # Pasar el objeto de página y los estados a la plantilla
    return render(request, 'listar_estudiante.html', {'page_obj': page_obj, 'estados': estados})



def seleccionar_estado(request):
    estudiante_id = request.POST.get('estudiante_id')
    estado_id = request.POST.get('kestado')
    
    estudiante = Estudiante.objects.get(pk=estudiante_id)
    estudiante.estado_id = estado_id
    estudiante.save()
    
    return redirect('listar_estudiante')
#CREAR CURSO

def crear_estado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        estado =  Estado.objects.create(
            nombre = nombre
        )
        return redirect('listar_estado')
    else:
        return render(request, 'estado/crear_estado.html')


#EDITAR CURSO

def editar_estado(request,id):
    
    estado = Estado.objects.get(id=id)
    
    if request.method == 'POST':
        
        nombre = request.POST.get('knombre')
        
        
        estado.nombre = nombre
        
        return redirect('listar_estado')
    
    return render(request, 'editar_estado.html', {'estado':estado})

#LISTAR CURSO

def listar_estado(request):
    estado = Estado.objects.all() 
    return render(request,'estado/listar_estado.html',{'estado':estado})




#ELIMINAR CURSO

def eliminar_estado(request,id):
    
    estado = Estado.objects.get(id=id)
    
    if request.method == 'GET':
        estado.delete()
        
    return redirect('listar_estado')
    
    
@csrf_exempt  # Deshabilita la protección CSRF
def cambiar_estado(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        nuevo_estado_id = data.get('estado')

        try:
            item = Estudiante.objects.get(id=item_id)
            item.estado_id = nuevo_estado_id
            item.save()
            return JsonResponse({'status': 'ok'})
        except Estudiante.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item no encontrado'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)