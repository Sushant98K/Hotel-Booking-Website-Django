from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    contactNo = models.CharField(max_length=15, blank=False)
    govId = models.CharField(max_length=128, blank=False)
    address = models.CharField(max_length=255, blank=False)