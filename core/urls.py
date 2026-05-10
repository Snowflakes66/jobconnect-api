"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# This is the main URL configuration file for the entire project.
# Django starts here when a request comes in and routes it to
# the correct app's urls.py based on the URL pattern.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django's built-in admin panel — available at /admin/
    # This gives us a powerful interface to manage all data
    # in the database without writing any extra code.
    path('admin/', admin.site.urls),

    # All account-related URLs (register, login, logout, profile)
    # are handled by the accounts app's urls.py.
    # include() tells Django to look inside accounts/urls.py
    # for the full list of URL patterns.
    path('api/', include('accounts.urls')),

    # All job-related URLs (list jobs, apply, applications etc.)
    # are handled by the jobs app's urls.py.
    path('api/', include('jobs.urls')),
]
