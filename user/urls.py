from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='base_panel/home.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='page-login.html'), name='login'),

    path('api_/profileUpdate/', ProfileUpdateAPIView.as_view(), name='Profile-Update'),
    path('api_/UserUpdate/', UserUpdateAPIView.as_view(), name='User-Update'),
    path('api_/UserRegistration/', UserCreateAPIView.as_view(), name='User-create'),
]
