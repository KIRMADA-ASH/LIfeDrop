from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

    path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),   # 👈 IMPORTANT
    path('recipient-dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
]