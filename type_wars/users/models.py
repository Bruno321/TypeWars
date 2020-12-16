from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class Profile(AbstractUser):
    points = models.IntegerField(default=0)
    victorys = models.IntegerField(default=0)
    defeats = models.IntegerField(default=0)