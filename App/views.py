from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from App.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from App.forms import formSetEstudiante


def inicio(request):
    return render(request, "App/inicio.html")

def curso(request):
    return render(request, "App/curso.html")

def profesores(request):
    return render(request, "App/profesor.html")

def estudiantes(request):
    Estudiantes = Estudiante.objects.all()
    return render(request, "App/estudiantes.html", {"Estudiantes":Estudiantes})

def setEstudiante(request):
    Estudiantes = Estudiante.objects.all()
    if request.method == 'POST':

        miFormulario = formSetEstudiante(request.POST)
        print(miFormulario)
        if miFormulario.is_valid:
            data = miFormulario.cleaned_data
            estudiante = Estudiante(nombre=data["nombre"],apellido=data["apellido"],email=data["email"])
            estudiante.save()
            miFormulario = formSetEstudiante()
            return render(request, "App/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes":Estudiantes})
    else:
        miFormulario = formSetEstudiante()
    return render(request, "App/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes":Estudiantes})

    """if request.method == 'POST':
        estudiante = Estudiante(nombre=request.POST["nombre"],apellido=request.POST["apellido"],email=request.POST["email"])
        estudiante.save()
        return render(request,"App/setEstudiantes.html",{"Estudiantes": Estudiantes})
    return render(request, "App/setEstudiantes.html", {"Estudiantes": Estudiantes})"""

def getProfesores(request):
    return render(request, "App/GetProfesores.html")

def buscarProfesor(request):
    nombre = request.GET["nombre"]
    if nombre:
        profesores = Profesor.objects.filter(nombre = nombre)
    return render(request, "App/GetProfesores.html", {"profesores" : profesores, "key": "value"})    

def loginWeb(request):
    if request.method == "POST":
        user = authenticate (username = request.POST['user'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return render(request, 'App/inicio.html')
        else:
            return render(request, 'App/login.html', {'error' : 'usuario o contraseña incorrecto'})
    else:
        return render(request, 'App/login.html')
    

def eliminarEstudiante(request, nombre_estudiante):
    estudiante = Estudiante.objects.get(nombre = nombre_estudiante)
    estudiante.delete()
    miFormulario = formSetEstudiante()
    Estudiantes = Estudiante.objects.all()
    return render(request, "App/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes":Estudiantes})

def editarEstudiante(request, nombre_estudiante):
    estudiante = Estudiante.objects.get(nombre= nombre_estudiante)

    if request.method == 'POST':
        miFormulario = formSetEstudiante(request.POST)
        if miFormulario.is_valid:
            data = miFormulario.cleaned_data

            estudiante.nombre = data['nombre']
            estudiante.apellido = data['apellido']
            estudiante.email = data['email']
            estudiante.save()
            miFormulario = formSetEstudiante()
            Estudiantes = Estudiante.objects.all()
            return render(request, "App/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes":Estudiantes})
    else:
        miFormulario = formSetEstudiante(initial={'nombre': estudiante.nombre, 'apellido': estudiante.apellido, 'email': estudiante.email})
    return render(request, "App/editarEstudiante.html", {"miFormulario":miFormulario})

def registro(request):
    if request.method == 'POST':
        userCreate = UserCreationForm(request.POST)
        if userCreate is not None:
            userCreate.save()
            return render (request, "App/login.html")
    else:
        return render(request, "App/registro.html")









