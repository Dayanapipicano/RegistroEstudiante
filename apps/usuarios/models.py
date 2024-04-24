from django.db import models

class Curso(models.Model):
    nombre = models.CharField( max_length=50)
    
    

class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    edad = models.IntegerField()
    estado = models.BooleanField(default=True)
    cursos = models.ForeignKey(Curso, on_delete=models.CASCADE)
    

class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    estudiantes = models.ManyToManyField(Estudiante)