from django.urls import path
from django.contrib.auth.views import LogoutView
from App.views import *

urlpatterns = [
    path('inicio', inicio, name="inicio"),
    path('cursos',curso, name="cursos"),
    path('estudiantes', estudiantes, name="estudiantes"),
    path('profesores', profesores, name="profesores" ),
    path('setEstudiante/', setEstudiante, name="setEstudiante"),
    path('getProfesores/', getProfesores, name="getProfesores"),
    path('buscarProfesor/', buscarProfesor, name="buscarProfesor"),
    path('login/', loginWeb, name="login"),
    path('eliminarEstudiante/<nombre_estudiante>', eliminarEstudiante, name="eliminarEstudiante"),
    path('editarEstudiante/<nombre_estudiante>', editarEstudiante, name="editarEstudiante"),
    path('registro/', registro, name="registro"),
    path('Logout/', CustomLogoutView.as_view(), name='Logout'),
    path('perfil/', perfilView, name="perfil"),
    path('perfil/editarPerfil/', editarPerfil, name="editarPerfil"),
    path('perfil/changePassword/', changePassword, name="changePassword"),
    path('perfil/avatar/', editAvatar, name="editAvatar"),
]
