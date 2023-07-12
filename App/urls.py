from django.urls import path
from App.views import *

urlpatterns = [
    path('inicio', inicio),
    path('cursos',curso, name="cursos"),
    path('estudiantes', estudiantes, name="estudiantes"),
    path('profesores', profesores, name="profesores" ),
    path('setEstudiante/', setEstudiante, name="setEstudiante"),
    path('getProfesores/', getProfesores, name="getProfesores"),
    path('buscarProfesor/', buscarProfesor, name="buscarProfesor"),
    path('login/', loginWeb, name="login"),
    path('eliminarEstudiante/<nombre_estudiante>', eliminarEstudiante, name="eliminarEstudiante"),
    path('editarEstudiante/<nombre_estudiante>', editarEstudiante, name="editarEstudiante"),
]
