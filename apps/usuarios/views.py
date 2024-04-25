import json
from django.shortcuts import render
from apps.usuarios.models import Estudiante
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.usuarios.models import Curso
from django.shortcuts import  redirect
from django.views.generic import  ListView


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
    
   
    if request.method == 'POST':
        nombre = request.POST.get('knombre')
        apellido = request.POST.get('kapellido')
        edad = request.POST.get('kedad')
        correo = request.POST.get('kcorreo')
   

        Estudiante.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            correo=correo,
           
        )
        
        return redirect('listar_estudiante')
    else:
        return render(request, 'registro.html')

#EDITAR ESTUDIANTE 

def editar_estudiante(request, id):
    
    estudiante =  Estudiante.objects.get(id=id)
    
    if request.method == 'POST':
        
        nombre = request.POST.get('knombre')
        apellido = request.POST.get('kapellido')
        edad = request.POST.get('kedad')
        correo = request.POST.get('kcorreo')
        
        
        
        estudiante.nombre = nombre
        estudiante.apellido = apellido
        estudiante.edad = edad
        estudiante.correo = correo

        estudiante.save()  
    
        return redirect('listar_estudiante')
    return render(request, 'editar_estudiante.html', {'estudiante':estudiante})


#LISTAR ESTUDIANTE -PAGINACION
def paginacion(request):
    estudiantes = Estudiante.objects.all()
    
    paginacion = Paginator(estudiantes,10)
    
    page_number = request.GET.get('page')
    page_obj = paginacion.get_page(page_number)
    return render(request,'listar_estudiante.html', {'page_obj':page_obj})


#PONER INACTIVO EL ESTUDIANTE 
def eliminar_estudiante(request,id):
    estudiante = Estudiante.objects.get(id=id)
    if request.method == 'GET':
        estudiante.estado = False
        estudiante.save()
        return redirect('listar_estudiante')
    
def activar_estudiante(request,id):
    estudiante = Estudiante.objects.get(id=id)
    if request.method == 'GET':
        estudiante.estado = True
        estudiante.save()
        return redirect('listar_estudiante')


#CREAR CURSO

def crear_curso(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        curso =  Curso.objects.create(
            nombre = nombre
        )
        return redirect('listar_curso')
    else:
        return render(request, 'curso/crear_curso.html')


#EDITAR CURSO

def editar_curso(request,id):
    
    curso = Curso.objects.get(id=id)
    
    if request.method == 'POST':
        
        nombre = request.POST.get('knombre')
        
        
        curso.nombre = nombre
        
        return redirect('listar_curso')
    
    return render(request, 'editar_curso.html', {'curso':curso})

#LISTAR CURSO

def listar_curso(request):
    curso = Curso.objects.all() 
    return render(request,'curso/listar_curso.html',{'curso':curso})




#ELIMINAR CURSO

def eliminar_curso(request,id):
    
    curso = Curso.objects.get(id=id)
    
    if request.method == 'GET':
        curso.delete()
        
    return redirect('listar_curso')
    
    
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