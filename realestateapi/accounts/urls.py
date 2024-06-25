# multi_role_auth/urls.py

from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
    # Add other URLs here
]