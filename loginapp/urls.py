from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('resetPass/', resetPass, name='resetPass'),
    path('updateAdmin/', updateAdmin, name='updateAdmin'),
    path('editAdmin/', editAdmin, name='editAdmin'),
]