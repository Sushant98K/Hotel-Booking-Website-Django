from django.urls import path
from .views import *

urlpatterns = [
    path('adduser/', addUser, name='adduser'),
    path('showuser/', showUsers, name='showuser'),
    path('updateuser/', updateUser, name='updateuser'),
    path('showuser/edit/<str:email>', editUser, name='edituser'),
    path('showuser/delete/<str:email>/', deleteUser , name='deleteuser'),
    path('profile/', viewProfile, name='profile'),

]