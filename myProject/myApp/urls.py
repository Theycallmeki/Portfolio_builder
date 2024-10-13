from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name=""),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('main/', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),

    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/<uidb64>/<token>/', views.password_reset, name='password_reset_confirm'),

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
    path('edit/<int:pk>/template2', views.Template2EditView, name='template2-edit'),
    path('delete/<int:pk>/template2', views.Template2DeleteView, name='template2-delete'),
    
    path('template3_create/', views.Template3CreateView, name='template3_create'),
    path('saved_template3/', views.template3_list, name='template3_list'),
    path('edit/<int:pk>/template3', views.Template3EditView, name='template3-edit'),
    path('delete/<int:pk>/template3', views.Template3DeleteView, name='template3-delete'),

    path('template4_create/', views.Template4CreateView, name='template4_create'),
    path('saved_template4/', views.template4_list, name='template4_list'),
    path('edit/<int:pk>/template4', views.Template4EditView, name='template4-edit'),
    path('delete/<int:pk>/template4', views.Template4DeleteView, name='template4-delete'),

    path('template5_create/', views.Template5CreateView, name='template5_create'),
    path('saved_template5/', views.template5_list, name='template5_list'),
    path('edit/<int:pk>/template5', views.Template5EditView, name='template5-edit'),
    path('delete/<int:pk>/template5', views.Template5DeleteView, name='template5-delete'),












]