# django
from django.urls import path

#local
from . import views

urlpatterns = [
    path('test/',views.game,name="game"),
    path('test/<str:game_game>',views.game_game,name="game_game"),
]