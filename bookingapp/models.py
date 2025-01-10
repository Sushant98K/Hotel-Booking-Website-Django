from django.db import models
from hotelapp.models import *
from userapp.models import *

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_category=models.ForeignKey(Category, on_delete=models.CASCADE)
    no_of_rooms=models.FloatField(default=0.0)
    no_of_people=models.IntegerField()
    check_in=models.DateTimeField()
    check_out=models.DateTimeField()
    total_price=models.FloatField(default=0.0)

class Order(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    subtotal = models.FloatField(default=0.0)
    status = models.CharField(max_length=50)
    orderId = models.CharField(max_length=50)