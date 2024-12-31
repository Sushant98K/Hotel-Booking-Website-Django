from django.urls import path
from .views import *

urlpatterns = [
    path('addhotel/', addhotel, name='addhotel'),
    path('show/', showHotel, name='showhotel'),
    path('updatehotel/', updateHotels, name='updatehotel'),
    path('show/edit/<int:id>', editHotels, name='edit'),
    path('show/delete/<int:id>', deleteHotels, name='delete'),
    path('show/category/<int:hotelId>', addCategory, name='addcategory'),
    path('show/clist/<int:hotelId>', cList, name='clist'),
    path('show/category/edit/<int:id>/', editCategory, name='editcategory'),
    path('show/category/delete/<int:id>/', deleteCategory, name='deletecategory'),
]
