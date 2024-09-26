from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('main/', views.main, name='main'),
    path('navbar/', views.navbar, name='navbar'),
    path('logout/', views.user_logout, name='logout'), 
    path('create/', views.create, name='create'),  # Ad # Ad

]