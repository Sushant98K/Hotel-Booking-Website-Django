from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def addhotel(request):
    if request.method == 'POST':
        hotelName = request.POST['hotelName']
        location = request.POST['location']
        hotelType = request.POST['hotelType']
        rating = request.POST['rating']
        contact = request.POST['contact']
        address = request.POST['address']
        hotel_image = request.FILES['hotel_image']
        # save data to the hotel table
        new_hotel = Hotel(
            hotelName=hotelName,
            location=location,
            hotelType=hotelType,
            rating=rating,
            contact=contact,
            address=address,
            hotel_image=hotel_image
        )
        new_hotel.save()
        
        return render(request, 'hotelapp/success.html', {'hotel': new_hotel, 'success_message': 'Hotel Added Successfuly!'})
    
    else:
        return render(request, 'hotelapp/AddHotel.html')

def showHotel(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotelapp/hotellist.html', {'hotels': hotels, 'current_page': 'hotellist'})

def updateHotels(request):
    if request.method == 'POST':
        # Use the same variable names as in addhotel
        hotelName = request.POST['hotelName']
        location = request.POST['location']
        hotelType = request.POST['hotelType']
        rating = request.POST['rating']
        contact = request.POST['contact']
        address = request.POST['address']
        hotelId = request.POST['hotelId']  # Assuming this is passed in the form
        hotel_image = request.FILES.get('hotel_image')

        # Retrieve the hotel instance
        try:
            hotel = Hotel.objects.get(hotelId=hotelId)
            # Update the fields
            hotel.hotelName = hotelName
            hotel.location = location
            hotel.hotelType = hotelType
            hotel.rating = rating
            hotel.contact = contact
            hotel.address = address
            
            # Only update the image if a new one is provided
            if hotel_image:
                hotel.hotel_image = hotel_image
            
            # Save the updated instance
            hotel.save()

            # Render the success template with the updated hotel information
            # return render(request, 'hotelapp/update_form.html', {'hotel': hotel, 'success_message': 'Update successful!'})
            return render(request, 'hotelapp/success.html', {'hotel':hotel, 'success_message': 'Hotel Updated Successfuly!'})
        except Hotel.DoesNotExist:
            return HttpResponse("<h1>Hotel not found</h1>")
    else:
        # Render the update form if the request method is not POST
        return render(request, 'hotelapp/update_form.html')
    

def editHotels(request, id):
        data=Hotel.objects.get(hotelId=id)
        return render(request, 'hotelapp/update_form.html', {'hotel': data})

def deleteHotels(request, id):
    hotel = Hotel.objects.get(hotelId=id)
    
    if request.method == 'POST':
        # If the user confirms the deletion
        hotel.delete()
        return HttpResponse("<h1>Success: Hotel Deleted!</h1>")
    
    return render(request, 'hotelapp/confirm_delete.html', {'hotel': hotel})

def addCategory(request, hotelId):
    if request.method != 'POST':
        data = Hotel.objects.get(hotelId=hotelId)
        return render(request, 'hotelapp/AddCategory.html', {'hotel_1': data})
    else:
        hotel = Hotel.objects.get(hotelId=hotelId)
        room_No=request.POST['room_No']
        roomType=request.POST['roomType']
        price_per_room=request.POST['price_per_room']
        available_rooms=request.POST['available_rooms']
        data_c=Category(hotel=hotel,room_No=room_No,roomType=roomType,price_per_room=price_per_room,available_rooms=available_rooms)
        data_c.save()
        return HttpResponse("<h1>success.......</h1>")

def cList(request, hotelId):
    hotel = Hotel.objects.get(hotelId=hotelId)
    cat_data = Category.objects.filter(hotel=hotel)
    return render(request, 'hotelapp/CategoryList.html', {'hotel_1': hotel, 'cat_data': cat_data,})

def editCategory(request, id):
    # Retrieve the category instance by ID
    category = Category.objects.get(id=id)
    
    if request.method == 'POST':
        # Update the category fields with the submitted data
        category.room_No = request.POST['room_No']
        category.roomType = request.POST['roomType']
        category.price_per_room = request.POST['price_per_room']
        category.available_rooms = request.POST['available_rooms']
        
        # Save the updated category
        category.save()
        
        return HttpResponse("<h1>Success: Category Updated!</h1>")
    
    # Render the edit form with the current category data
    return render(request, 'hotelapp/editCategory.html', {'category': category})

# In hotelapp/views.py

def deleteCategory(request, id):
    # Retrieve the category instance by ID
    category = Category.objects.get(id=id)
    
    if request.method == 'POST':
        # If the user confirms the deletion
        category.delete()
        return HttpResponse("<h1>Success: Category Deleted!</h1>")
    
    # Render the confirmation template
    return render(request, 'hotelapp/confirm_delete_category.html', {'category': category})