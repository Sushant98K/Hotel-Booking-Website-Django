from django.urls import path
from .views import *

urlpatterns = [
    path('home/', index, name='home'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('package/', package, name='package'),
    path('contact/', contact, name='contact'),
    path('destination/', destination, name='destination'),
    path('booking/', booking, name='booking'),
    path('team/', team, name='team'),
    path('testimonial/', testimonial, name='testimonial'),
    path('error/', error, name='error'),
    
]