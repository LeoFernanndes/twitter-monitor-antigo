from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class ArrobaModel(models.Model):
    arroba = models.CharField(max_length=100)
    last_query_date = models.DateField(default=datetime.now, blank=True)
    profile_image_url = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)