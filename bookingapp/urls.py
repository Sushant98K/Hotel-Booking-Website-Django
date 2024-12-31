from django.urls import path
from .views import *

urlpatterns = [
    path("booking/<int:id>", addBooking, name="booking"),
]