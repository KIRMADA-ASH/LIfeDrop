from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_blood, name='request_blood'),
    path('status/', views.request_status, name='request_status'),
]