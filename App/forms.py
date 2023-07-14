from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class formSetEstudiante(forms.Form):
    nombre = forms.CharField(max_length=30)
    apellido = forms.CharField(max_length=30)
    email = forms.EmailField()

class LoginForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm():
    username = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Email"}))
    first_name = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"First Name"}))
    last_name = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Last Name"}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={"placeholder":"Password"}))

    class meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        help_texts = { k:"" for k in fields}




