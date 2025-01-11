from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from hotelapp.models import *
from userapp.models import *
from .models import *
import razorpay

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
    sessionemail = request.session['custemail']
     
    
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        status = 'started..'
        subtotal = sum_total
        razorpay_key = settings.RAZORPAY_KEY_ID
        
        new_booking = Order(
            user = user,
            fname = fname,
            lname = lname,
            email = email,
            phone = phone,
            status = status,
            subtotal = subtotal, 
        )
        new_booking.save()
        
        current_date = datetime.now().strftime("%Y%m%d")
        new_booking.orderId = f"{current_date}{new_booking.id}"
        new_booking.save()
        razorpay_amount = int(subtotal * 100)  # Convert to integer for Razorpay
        
        #authorizee razorpay client with API keys
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        
        currency = 'INR'
        amount = razorpay_amount
        
        #create razorpay Order
        razorpay_order = razorpay_client.order.create(
            dict(
                amount=amount, 
                currency=currency, 
                payment_capture='0',
                notes={
                    'custemail': sessionemail,  # Pass session email to Razorpay
                        }
                )
            )
        
        #order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        
        
        #we need to pass these details to frontend
        
        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'sessionemail': sessionemail,
            'domain': request.get_host(),  # Dynamic domain
        }
        
        
        return render(request, 'bookingapp/payment.html', locals())
    else:
        return render(request, 'bookingapp/checkout.html', locals())
    

def payment(request):
    return render(request, 'bookingapp/payment.html', locals())

def paymentsuccess(request):
    
    # email=request.GET.get("email")
    sessionemail = request.session.get('custemail')
    user = User.objects.get(email=request.session['custemail'])
    
    if not sessionemail:
        # If the email is not found, return an error message or redirect
        return HttpResponse("<h1>Error: Email not found in session</h1>")
    
    # Retrieve payment details from Razorpay callback
    payId = request.GET.get('payment_id')
    tbill = request.GET.get('total_bill')
    order_no = request.GET.get('order_id')
    invoice_date = datetime.now()
    
    
    try:
        # Retrieve the Order object using the order_id
        order = Order.objects.get(orderId=order_no)

        # Update the status field to "payment success"
        order.status = "payment success"
        order.save()

        # Retrieve the user associated with the order
        user = User.objects.get(email=sessionemail)
        booking_data = Booking.objects.filter(user=user)
        total = sum(item.total_price for item in booking_data)
        tax = total * 0.15
        sum_total = total + tax

        # Delete all Booking entries related to the user
        # Booking.objects.filter(user=user).delete()

    except Exception as e:
        # Handle the case where the Order or User does not exist
        return HttpResponse("<h1>Error: Order or User not found</h1>")
    
    
    
    
    subject = "To book hotel"
    email_body = f"Payment Id: {payId}\nOrder No: {order_no}\nTotal Bill: {tbill}\nEmail: {sessionemail}"
    from_email=settings.EMAIL_HOST_USER
        
    fail_silently = False
        
    send_mail(subject=subject, message=email_body, from_email=from_email, recipient_list=["sushant98k@gmail.com"])
        
    # return HttpResponse("<h1>Payment success......</h1>")
    return render(request, 'bookingapp/paymentsuccess.html', locals())