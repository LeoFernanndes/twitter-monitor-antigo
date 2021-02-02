from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class ArrobaModel(models.Model):
    arroba = models.CharField(max_length=100)
    last_query_date = models.DateField(default=datetime.now, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)