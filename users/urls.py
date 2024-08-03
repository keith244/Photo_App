from django.urls import path
from . import views

urlpatterns =[
    path('login/',views.ilogin, name='login'),
    path('register/',views.iregister, name='register'),
    path('logout/',views.ilogout, name='logout'),
]