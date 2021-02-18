from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import *


rout=DefaultRouter()
rout.register('user', UserAPIView, basename='user')

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='base_panel/home.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='page-login.html'), name='login'),
    path('registration/', registration, name='User-create'),

    path('_api/', include(rout.urls)),

    path('_api/profileUpdate/', ProfileUpdateAPIView.as_view(), name='Profile-Update'),
    path('_api/PassUpdate/', PasswordChangeAPIView.as_view(), name='Pass-Update'),
]
