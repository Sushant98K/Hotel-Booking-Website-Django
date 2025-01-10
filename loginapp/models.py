from django.db import models

# Create your models here.


class Admin(models.Model):
    email = models.EmailField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)