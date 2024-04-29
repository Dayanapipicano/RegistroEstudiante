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
from apps.usuarios.views import crear_estado,listar_estado,principal, paginacion, editar_estudiante, editar_estado,eliminar_estado,registrar_estudiante,seleccionar_estado
from apps.usuarios import views
from apps.usuarios.views import principal


urlpatterns = [
    path('admin/', admin.site.urls),

    

    #ESTUDIANTE
    path('inidex',principal.as_view(),name='inicio'),
    path('',registrar_estudiante,name='registrar'),
    path('editar_estudiante/<int:id>',editar_estudiante,name='editar_estudiante'),

    path('listar_estudiente', paginacion, name='listar_estudiante'),

    
    #CURSO
    path('crear_estado', crear_estado, name='crear_estado'),
    path('listar_estado', listar_estado, name='listar_estado'),
    path('editar_estado/<int:id>', editar_estado, name='editar_estado'),
    path('eliminar_estado/<int:id>', eliminar_estado, name='eliminar_estado'),
    
    path('cambiar_estado/<int:item_id>/', views.cambiar_estado, name='cambiar_estado'),
    path('seleccionar/', seleccionar_estado, name='seleccionar_estado'),
]
