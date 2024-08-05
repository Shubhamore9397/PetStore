from django.db import models

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=100)