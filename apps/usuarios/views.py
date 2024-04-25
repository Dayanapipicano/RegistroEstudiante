from django.shortcuts import render
from apps.usuarios.models import Estudiante
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.usuarios.models import Curso
from django.shortcuts import  redirect
from django.views.generic import  ListView



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
            correo=correo
        )

        return redirect('listar_estudiante')


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
    
    
