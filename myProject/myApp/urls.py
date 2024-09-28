from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('main/', views.main, name='main'),

    path('profile/', views.profile, name='profile'),
    path('navbar/', views.navbar, name='navbar'),
    path('logout/', views.user_logout, name='logout'), 
    path('create/', views.create, name='create'),  # Ad # Ad
    path('creates/', views.create_portfolio, name='create_portfolio'),
    path('edit/<int:portfolio_id>/', views.edit_portfolio, name='edit_portfolio'),
    path('portfolios/delete/<int:portfolio_id>/', views.delete_portfolio, name='delete_portfolio'),
    path('portfolios/', views.portfolio_list, name='portfolio_list'),  # For function-based view
    path('ckeditor/upload/', views.upload_image, name='upload_image'),

    path('template1_create/', views.Template1CreateView, name='template1_create'),
    path('saved_template1/', views.template1_list, name='template_list'),
    path('edit/<int:pk>/template', views.Template1EditView, name='template1-edit'),
    path('delete/<int:pk>/template', views.Template1DeleteView, name='template1-delete'),

    path('template2_create/', views.Template2CreateView, name='template2_create'),
    path('saved_template2/', views.template2_list, name='template2_list'),










]