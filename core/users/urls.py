from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('become-creator/', views.become_creator, name='become_creator'),
    path('logout/', views.custom_logout, name='logout'),
]