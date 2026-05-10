# This file maps URL patterns to the account-related views.
# All authentication endpoints live here — register, login, logout, profile.

from django.urls import path
from . import views

# Namespace for the accounts app URLs.
# Helps avoid naming conflicts with other apps.
app_name = 'accounts'

urlpatterns = [
    # POST /auth/register/ — Create a new user account
    # Anyone can access this — no token required
    path('auth/register/', views.RegisterView.as_view(), name='register'),

    # POST /auth/login/ — Log in and receive an authentication token
    # Anyone can access this — no token required
    path('auth/login/', views.LoginView.as_view(), name='login'),

    # POST /auth/logout/ — Log out and invalidate the current token
    # Must be logged in to access this
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),

    # GET /auth/profile/ — View the currently logged-in user's profile
    # Must be logged in to access this
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),
]