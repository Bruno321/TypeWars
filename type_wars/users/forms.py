from django import forms
from django.forms import ModelForm
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,min_length=1,label='Ingresa tu correo',required=True,widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}))
    password = forms.CharField(max_length=50,min_length=1,label='Ingresa tu contraseña',required=True,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))

class RegisterForm(ModelForm):
     
     class Meta:
         model = Profile
         fields = ['username','email','password']

         widgets = {
             'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa el usuario que tendras'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'correo@correo.com'}),   
            'password': forms.PasswordInput(render_value=True,attrs={'class':'form-control','placeholder':'Ingresa la contraseña','style':'margin-bottom:30px'}),
         }