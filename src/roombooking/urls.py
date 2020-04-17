"""roombooking URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from users.views import (
    home_page,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('bookings/', include('bookings.urls')),
    path('buildings/', include('buildings.urls')),
    path('companies/', include('companies.urls')),

    # Start page
    path('', home_page, name='home'),
]
