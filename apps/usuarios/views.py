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

#PONER INACTIVO EL ESTUDIANTE 
def haciendo_estudiante(request,id,):
    
    estudiante = get_object_or_404(Estudiante, id=id)

    if request.method == 'GET':
        # Obtener el estado actual del estudiante
        estado_actual = estudiante.estado

        # Actualizar el estado del estudiante según el estado actual
        if estado_actual == 'por hacer':
            estudiante.estado = 'haciendo'
        elif estado_actual == 'finalizado':
            estudiante.estado = 'haciendo'

        # Guardar los cambios en la base de datos
        estudiante.save()

        # Redirigir a la página que muestra la lista de estudiantes
        return redirect('listar_estudiante')

    
def por_hacer_estudiante(request,id):
    estudiante = Estudiante.objects.get(id=2)
    if request.method == 'GET':
        estudiante.estado = 'por hacer'
        estudiante.save()
        return redirect('listar_estudiante')

def finalizado_estudiante(request,id):
    estudiante = Estudiante.objects.get(id=3)
    if request.method == 'GET':
        estudiante.estado = 'finalizado'
        estudiante.save()
        return redirect('listar_estudiante')

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
    
    
@csrf_exempt  # Permite solicitudes POST sin token CSRF
@require_http_methods(['POST'])
def cambiar_estado(request, item_id):
    try:
        item = Estudiante.objects.get(id=item_id)
        data = json.loads(request.body)  # Obtener datos de la solicitud
        item.estado = data['estado']  # Cambiar el estado
        item.save()  # Guardar cambios

        return JsonResponse({'success': 'Estado actualizado'}, status=200)

    except Estudiante.DoesNotExist:
        return JsonResponse({'error': 'Objeto no encontrado'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)