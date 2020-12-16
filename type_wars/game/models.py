from django.db import models

# Create your models here.
class Games(models.Model):
    game_name = models.CharField(max_length=100)