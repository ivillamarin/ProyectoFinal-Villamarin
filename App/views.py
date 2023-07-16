from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from App.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, login as django_login, update_session_auth_hash
from App.forms import formSetEstudiante, LoginForm, UserEditForm, changePasswordForm, AvatarForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User






def inicio(request):
    avatar = getavatar(request)
    return render(request, "App/inicio.html", {"avatar" : avatar})

def curso(request):
    return render(request, "App/curso.html")

@login_required
def profesores(request):
    return render(request, "App/profesor.html")

@login_required
def estudiantes(request):
    Estudiantes = Estudiante.objects.all()
    return render(request, "App/estudiantes.html", {"Estudiantes":Estudiantes})

@login_required
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
    error = None 
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                error = 'Usuario o contraseña incorrectos'
    
    else:
        form = LoginForm()
    
    return render(request, 'App/login.html', {'form': form, 'error': error})

        
    
    form = AuthenticationForm()
    return render(request, 'App/login.html', {'form': form})
    

def eliminarEstudiante(request, nombre_estudiante):
    estudiante = Estudiante.objects.get(nombre=nombre_estudiante)
    estudiante.delete()
    miFormulario = formSetEstudiante()
    Estudiantes = Estudiante.objects.all()
    return render(request, "App/setEstudiantes.html", {"miFormulario": miFormulario, "Estudiantes": Estudiantes})

def editarEstudiante(request, nombre_estudiante):
    estudiante = Estudiante.objects.get(nombre=nombre_estudiante)

    if request.method == 'POST':
        miFormulario = formSetEstudiante(request.POST)
        if miFormulario.is_valid():  # Se corrigió la validación del formulario
            data = miFormulario.cleaned_data

            estudiante.nombre = data['nombre']
            estudiante.apellido = data['apellido']
            estudiante.email = data['email']
            estudiante.save()
            miFormulario = formSetEstudiante()
            Estudiantes = Estudiante.objects.all()
            return render(request, "App/setEstudiantes.html", {"miFormulario": miFormulario, "Estudiantes": Estudiantes})
    else:
        miFormulario = formSetEstudiante(initial={'nombre': estudiante.nombre, 'apellido': estudiante.apellido, 'email': estudiante.email})
    return render(request, "App/editarEstudiante.html", {"miFormulario": miFormulario})

def registro(request):
    if request.method == 'POST':
        userCreate = UserCreationForm(request.POST)
        if userCreate.is_valid():
            user = userCreate.save()
            login(request, user)
            return redirect('inicio')
    else:
        userCreate = UserCreationForm()
    return render(request, 'App/registro.html', {'form': userCreate})

class CustomLogoutView(LogoutView):
    template_name = 'App/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

@login_required
def perfilView(request):
    return render(request, 'App/perfil/perfil.html')

@login_required
def editarPerfil(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            return render(request, 'App/perfil/perfil.html')
    else:
        form = UserEditForm(initial = {'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name })
        return render(request, 'App/perfil/editarPerfil.html', {"form": form})
    
@login_required
def changePassword(request):
    usuario = request.user
    if request.method == 'POST':
        form = changePasswordForm(data = request.POST, user = usuario)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
        return render(request, "App/inicio.html")
    else:
        form = changePasswordForm(user = usuario)
        return render ( request, 'App/perfil/changePassword.html', {"form": form} )
    
def editAvatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user = User.objects.get(username = request.user)
            avatar = Avatar(user = user, image = form.cleaned_data['avatar'], id = request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, "App/inicio.html", {'avatar' : avatar} )
    else:
        try:
            avatar = Avatar.objects.filter(user = request.user.id)
            form = AvatarForm()
        except:
            form = AvatarForm()
    return render (request, "App/perfil/avatar.html", {'form': form})

def getavatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return avatar

@login_required
def comentarios(request):
    if request.method == 'POST':
        nuevo_comentario = request.POST.get('nuevo_comentario', '')
        # Aquí puedes realizar cualquier lógica adicional, como guardar el comentario en la base de datos.

        # Ejemplo: Guardar el comentario en una lista en memoria
        comentarios_guardados = request.session.get('comentarios', [])
        comentarios_guardados.append(nuevo_comentario)
        request.session['comentarios'] = comentarios_guardados

    comentarios = request.session.get('comentarios', [])  # Obtener los comentarios guardados

    return render(request, 'App/comentarios.html', {'comentarios': comentarios})


def acercaDeMi(request):
    return render(request, 'App/acercaDeMi.html')









    