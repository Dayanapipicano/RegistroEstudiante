"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.usuarios.views import crear_curso,listar_curso,principal, paginacion, editar_estudiante, editar_curso, eliminar_estudiante, eliminar_curso,registrar_estudiante
from apps.usuarios import views
from apps.usuarios.views import principal


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',principal.as_view(),name='inicio'),
    

    #ESTUDIANTE
    path('',principal.as_view(),name='inicio'),
    path('registrar/',registrar_estudiante,name='registrar'),
    path('editar_estudiante/<int:id>',editar_estudiante,name='editar_estudiante'),
    path('eliminar_estudiante/<int:id>',eliminar_estudiante,name='eliminar_estudiante'),
    path('listar_estudiente', paginacion, name='listar_estudiante'),

    
    #CURSO
    path('crear_curso', crear_curso, name='crear_curso'),
    path('listar_curso', listar_curso, name='listar_curso'),
    path('editar_curso/<int:id>', editar_curso, name='editar_curso'),
    path('eliminar_curso/<int:id>', eliminar_curso, name='eliminar_curso'),
]
