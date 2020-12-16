# django
from django.urls import path

#local
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('login/',views.loginn, name="login")
]