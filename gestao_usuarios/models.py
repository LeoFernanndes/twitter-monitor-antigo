from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ArrobaModel(models.Model):
    arroba = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)