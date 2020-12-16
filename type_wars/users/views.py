#  django
from django.shortcuts import render,  HttpResponse,redirect
from django.contrib.auth import get_user_model,authenticate, login, logout
from django.contrib.auth.models import User

# local
from game.models import Games
from .models import Profile
from .forms import LoginForm, RegisterForm

# python
import random
import string


def index(request):
    
    """
        TODO VALIDAR QUE SOLO SE PUEDA  ACCEDER AL GAME DESDE CIERTA URL, BLOQUEAR LAS DEMAS CONEXIONES
        CORRER ALV A ALGUIEN SI LA SALA YA TIENE 2 VATOS
        HACER LOGIN Y REGISTER EN LA MISMA PAGINA
        
    """
    if request.method == 'POST':

        # Usar id del juego en vez de nombre

        # Checar si existe alguien mas que haya echo este post
        if (len(Games.objects.all())>0):
            # si hay
            game_name = Games.objects.get()
            # borramos la partida de la db 
            true_game_name = game_name.game_name
            game_name.delete()
            return render(request,'index.html',{'game_name':true_game_name})
        else:
            # No hay juegos entonces lo creamos
            letters = string.ascii_letters
            game_name = ''.join(random.choice(letters) for i in range(8))

            game = Games(game_name=game_name)
            game.save()
            # Mandamos al usuario a su partida
            return render(request,'index.html',{'game_name':game_name})
        
    else:
        return render(request,'index.html')
    # print(uuid.uuid4())

    # if request.user.is_authenticated:
    #     print("Estas logeado")
    #     if request.user.is_anonymous:
    #         print("Logeado pero anonimo")
    #     else:
    #         print("Logeado con cuenta permanente")
    # else:
    #     print("No estas logeado")

    # print(request.COOKIES)

    # if not request.COOKIES.get('game_name'):
    #     response = render(request,'index.html')
    #     response.set_cookie('game_name',uuid.uuid4())
    #     return response
    # else:
    #     response = render(request,'index.html')
    #     response.set_cookie('game_name',uuid.uuid4())
    #     return response    

def loginn(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect(index)
            else:
                form.add_error(None,'Revisa tus datos gordito')
                return render(request,'login.html',{'form':form})
        else:
            return HttpResponse('Revisa tus datos')

    else:
        form = LoginForm()
        return render(request,'login.html',{'form':form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User = get_user_model()
            #  CHECAR OTRA FORMA DE HACERLO SIN TANTO QUERY
            user = User.objects.filter(username=username)
            email_user = User.objects.filter(email=email)

            if(len(user)>0):
                form.add_error('username','Este nombre ya esta registrado')

                return render(request,'registro.html',{'form':form})

            if(len(email_user)>0):
                form.add_error('email','Este correo ya esta registrado')

                return render(request,'registro.html',{'form':form}) 

            user = User(username=username,email=email)
            user.set_password(password)
            user.save()

            user_to_auth = authenticate(username=username, password=password)
            if user_to_auth is not None:
                login(request,user_to_auth)
                return redirect(index)
            else:
                form.add_error(None,'Usuario o contraseña incorrectos')
                return render(request,'register.html',{'form':form})


            form.add_error(None,'Usuario creado exitosamente')

            return render(request,'register.html',{'form':form})

        else:
            return HttpResponse('revisa tus datos')
    else:
        form = RegisterForm()
        return render(request,'register.html',{'form':form})

    