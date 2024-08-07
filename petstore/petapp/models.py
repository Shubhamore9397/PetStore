from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=100)
    
class Cart(models.Model):
    pid= models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='pid')
    uid= models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid')
    quantity= models.IntegerField(default=1)