from django.shortcuts import render


def index(request):
    return render(request, 'frontendapp/index.html', {'current_page': 'home'})

def about(request):
    return render(request, 'frontendapp/about.html', {'current_page': 'about'})

def service(request):
    return render(request, 'frontendapp/service.html', {'current_page': 'service'})

def package(request):
    return render(request, 'frontendapp/package.html', {'current_page': 'package'})

def contact(request):
    return render(request, 'frontendapp/contact.html', {'current_page': 'contact'})

def destination(request):
    return render(request, 'frontendapp/destination.html', {'current_page': 'destination'})

def booking(request):    
    return render(request, 'frontendapp/booking.html', {'current_page': 'booking'})

def team(request):
    return render(request, 'frontendapp/team.html', {'current_page': 'team'})

def testimonial(request):
    return render(request, 'frontendapp/testimonial.html', {'current_page': 'testimonial'})

def error(request):
    return render(request, 'frontendapp/error.html', {'current_page': 'error'})