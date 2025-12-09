from django.urls import path
from . import views

urlpatterns =[
    path('login/',views.ilogin, name='login'),
    path('register/',views.iregister, name='register'),
    path('logout/',views.ilogout, name='logout'),
    path('profile/<str:username>/',views.profile, name='profile'),
    path('profile_view/',views.profile_view, name='profile_view'),

]