from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from App.models import *


def inicio(request):
    return render(request, "App/inicio.html")

def curso(request):
    return render(request, "App/curso.html")

def profesores(request):
    return render(request, "App/profesor.html")

def estudiantes(request):
    return render(request, "App/estudiantes.html")

def setEstudiante(request):
    if request.method == 'POST':
        estudiante = Estudiante(nombre=request.POST["nombre"],apellido=request.POST["apellido"],email=request.POST["email"])
        estudiante.save()
        return render(request,"App/inicio.html")
    return render(request, "App/setEstudiantes.html")

def getProfesores(request):
    return render(request, "App/GetProfesores.html")

def buscarProfesor(request):
    nombre = request.GET["nombre"]
    if nombre:
        profesores = Profesor.objects.filter(nombre = nombre)
    return render(request, "App/GetProfesores.html", {"profesores" : profesores})    

