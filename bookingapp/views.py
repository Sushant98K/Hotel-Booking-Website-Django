from django.shortcuts import render
from hotelapp.models import *
from userapp.models import *

def addBooking(request,id):
    if request.method !=' POST':
        cat_data=Category.objects.get(id=id)
        return render(request, 'bookingapp/AddBooking.html', {'cat_data':cat_data})
        