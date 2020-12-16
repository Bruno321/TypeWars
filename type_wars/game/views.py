from django.shortcuts import render
from django.http import  HttpResponse

from .models import Games

import requests
import random
import json
import random
import string
# Create your views here.
def game(request):

    games = Games.objects.all()

    if (len(games)>0):
        print("Si hay juegos")

    else:
        print(request.COOKIES['game_name'])
        print("No hay juegos")

    
    return HttpResponse('hola')

def game_game(request,game_game):
    
    # response = requests.get('https://api.datamuse.com/words?ml=duck&sp=b*&max=10')
    # print(response.json())
    # https://api.datamuse.com/words?sp=*a?? buenarda, terminen con a y y entre mas signos d interrogacion mas cambia
    # no usar enmpieza con, da las mismas 
    # ???????? 8 signos maximos aveces se rompe jasjas
    """
        API doc: https://www.datamuse.com/api/
        ml= means like
        sp= spelled like b* starts with letter b, *a ends with letter a
        max=max results
    """
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    letter_to_send = alphabet[random.randint(0,25)]
    simbol = ['?','??','???','????']
    simbol_to_send = simbol[random.randint(0,3)]
    # payload = {'ml':'duck','sp':'b*','max':'10'}

    payload = {'sp':'*'+letter_to_send+simbol_to_send}

    response = requests.get('https://api.datamuse.com/words',params=payload)
    # print(response)
    # print(response.json())

    words = response.json()
    words_list = json.dumps(words)
    # print(type(json.dumps(words)))
    # print(type(words))

    letters = string.ascii_letters
    raw_id = ''.join(random.choice(letters) for i in range(4))

    if request.user.is_anonymous:
        username = 'Guest' + '/' + raw_id
    else:
        username = request.user.username + '/' + raw_id

    return render(request,'game.html',{'game_name':game_game,'username':username,'words':words_list})