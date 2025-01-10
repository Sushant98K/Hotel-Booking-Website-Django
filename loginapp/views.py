from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .models import *
from userapp.models import *

def login(request):
    if request.method == 'POST':
        type = request.POST['type']
        email = request.POST['email']
        password = request.POST['password']
        
        if type == 'user':
            try:                                                        #to ensure the email are in the database
                cust = User.objects.get(email=email)
                if cust:
                    flag = check_password(password, cust.password)
                    if flag:
                        request.session['custemail']= email
                        return redirect('home')  # Redirect to the home list after login

                        
                        # return HttpResponse("<h1>User Log In successful</h1>")
                    else:
                        return HttpResponse("<h1>Invalid User password</h1>")
            except:
                return redirect('login')
            
                
        elif type == 'admin':
            try:                                                        #to ensure the email are in the database
                admin = Admin.objects.get(email=email)
                if admin:
                    
                    if password == admin.password:
                        request.session['adminemail']= email
                        return redirect('home') # Redirect to the home after login
                        
                        # return HttpResponse("<h1>Admin Log In successful</h1>")
                    else:
                        return HttpResponse("<h1>Invalid Admin password</h1>")
            except:
                return redirect('login')

    else:
        return render(request, 'loginapp/login.html')


def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect('home')

def resetPass(request):
    return render(request, 'loginapp/resetpassword.html')

def updateAdmin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            try:
                admin = Admin.objects.get(email=email)
                admin.email = email
                admin.password = make_password(password)
                admin.save()
                return HttpResponse("<h1>Password Updated Successfully</h1>")
            except:
                return HttpResponse("<h1>Admin not found</h1>")
    else:
        return render(request, 'loginapp/editadmin.html')

def editAdmin(request):
    email = request.session['adminemail']
    admin = Admin.objects.get(email=email)
    return render(request, 'loginapp/editadmin.html', {'admin': admin})
    

