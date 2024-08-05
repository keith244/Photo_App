from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('create_post/',views.create_post,name='create_post'),
    path('profile/<str:username>/',views.profile, name='profile'),
    path('profile_view/',views.profile_view, name='profile_view'),
    path('photo_details/<int:post_id>/',views.post_details, name='photo_details'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]