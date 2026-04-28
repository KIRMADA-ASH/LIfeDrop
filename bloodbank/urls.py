from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('donor.urls')),
    path('', include('inventory.urls')),
    path('', include('recipient.urls')),
]
