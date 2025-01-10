from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from hotelapp.models import *
from userapp.models import *
from .models import *

def addBooking(request, id):
    if request.method == 'POST':
        # Retrieve the category instance
        cat_data = Category.objects.get(id=id)
        
        # Retrieve the user instance (assuming the user is logged in)
        email= request.session['custemail']
        user = User.objects.get(email=email)  # Adjust this based on your authentication logic
        
        # Retrieve form data
        no_of_rooms = request.POST['no_of_rooms']
        no_of_people = request.POST['no_of_people']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        total_price = float(no_of_rooms) * cat_data.price_per_room
        
        # Create and save the booking instance
        booking = Booking(
            user=user,
            hotel=cat_data.hotel,
            room_category=cat_data,
            no_of_rooms=no_of_rooms,
            no_of_people=no_of_people,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price
        )
        booking.save()
        
        return redirect('bookinglist')  # Redirect to the booking list page after successful booking
    else:
        cat_data = Category.objects.get(id=id)
        return render(request, 'bookingapp/AddBooking.html', {'cat_data': cat_data})

def bookingList(request):
    # Retrieve all bookings for the logged-in user
    email= request.session['custemail']
    user = User.objects.get(email=email)  # Adjust this based on your authentication logic
    bookings = Booking.objects.filter(user=user)
    return render(request, 'bookingapp/BookingList.html', {'bookings': bookings})

def deleteBooking(request, id):
    # Retrieve the booking instance by ID
    booking = Booking.objects.get(id=id)
    
    if request.method == 'POST':
        # Delete the booking
        booking.delete()
        return redirect('bookinglist')  # Redirect to the booking list after deletion
    
    # Render a confirmation template (optional)
    return render(request, 'bookingapp/confirm_delete_booking.html', {'booking': booking})

def checkout(request):
    
    user = User.objects.get(email=request.session['custemail'])
    booking_data = Booking.objects.filter(user = user)
    total = sum(item.total_price for item in booking_data)
    tax = total * 0.15
    sum_total = total + tax
     
    
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        status = 'started..'
        subtotal = sum_total
        razorpay_key = settings.RAZORPAY_KEY_ID
        
        new_booking = Order(
            fname = fname,
            lname = lname,
            email = email,
            phone = phone,
            status = status,
            subtotal = subtotal, 
        )
        # new_booking.save()
        
        current_date = datetime.now().strftime("%Y%m%d")
        new_booking.orderId = f"{current_date}{new_booking.id}"
        # new_booking.save()
        razorpay_amount = subtotal * 100
        return render(request, 'bookingapp/payment.html', locals())
    else:
        return render(request, 'bookingapp/checkout.html', locals())
    

def payment(request):
    return render(request, 'bookingapp/payment.html', locals())