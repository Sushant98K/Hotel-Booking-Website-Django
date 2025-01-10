from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password 
from django.http import HttpResponse
from bookingapp.models import *
from loginapp.models import *
from .models import *

# Create your views here.
def addUser(request):
    if request.method=='POST':
        email = request.POST['email']
        username = request.POST['username']
        password = make_password(request.POST['password'])  #apply make password to encrypt the password
        contactNo = request.POST['contactNo']
        govId = request.POST['govId']
        address = request.POST['address']
        
        new_user = User(
            email=email,
            username=username,
            password=password,
            contactNo=contactNo,
            govId=govId,
            address=address
        )
        new_user.save()
        
        return render(request, 'userapp/success.html', {'user': new_user, 'success_message': 'User Added Successfully!','current_page': 'adduser' })
    else:
        return render(request, 'userapp/AddUser.html')

def showUsers(request):
    users = User.objects.all()
    return render(request, 'userapp/showUsers.html', {'users': users})

def updateUser(request):
    if request.method == 'POST':
        # Use the same variable names as in addUser 
        email = request.POST['email']  # Assuming this is passed in the form
        username = request.POST['username']
        password = request.POST['password']
        contactNo = request.POST['contactNo']
        govId = request.POST['govId']
        address = request.POST['address']

        # Retrieve the user instance
        try:
            user = User.objects.get(email=email)
            # Update the fields
            user.username = username
            user.password = password
            user.contactNo = contactNo
            user.govId = govId
            user.address = address
            
            # Save the updated instance
            user.save()

            # Render the success template with the updated user information
            return render(request, 'userapp/success.html', {'user': user, 'success_message': 'User  Updated Successfully!'})
        except User.DoesNotExist:
            return HttpResponse("<h1>User not found</h1>")
    else:
        # Render the update form if the request method is not POST
        return render(request, 'userapp/update_user.html')
def editUser(request, email):
        user=User.objects.get(email=email)
        return render(request, 'userapp/update_user.html', {'user': user})
    
    
def deleteUser (request, email):
    try:
        user = User.objects.get(email=email)  # Get user by email
    except User.DoesNotExist:
        return HttpResponse("<h1>User not found</h1>")

    if request.method == 'POST':
        user.delete()  # Delete the user
        return redirect('showuser')  # Redirect to the user list after deletion

    return render(request, 'userapp/confirm_delete.html', {'user': user})  # Render confirmation template

def viewProfile(request):
    # Retrieve the user instance (assuming the user is logged in)
    custemail = request.session.get('custemail')
    adminemail = request.session.get('adminemail')
    
    if custemail:
        user = User.objects.get(email=custemail)
        return render(request, 'userapp/profile.html', {'user_data': user})
    elif adminemail:
        admin = Admin.objects.get(email=adminemail)
        return render(request, 'userapp/profile.html', {'user_data': admin})
    else:
        return HttpResponse("<h1>You are not logged in</h1>")
