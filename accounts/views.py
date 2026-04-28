from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import CustomUser


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user_type = request.POST.get('user_type', '').strip().lower()

        if not username or not password or user_type not in dict(CustomUser.USER_TYPES):
            messages.error(request, 'Please provide a valid username, password, and user type.')
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        CustomUser.objects.create_user(
            username=username,
            password=password,
            user_type=user_type,
        )

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 'donor':
                return redirect('donor_dashboard')
            return redirect('recipient_dashboard')

        messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


@login_required
def donor_dashboard(request):
    if request.user.user_type != 'donor':
        messages.error(request, 'Only donors can access this dashboard.')
        return redirect('recipient_dashboard')
    return render(request, 'donor_dashboard.html')


@login_required
def recipient_dashboard(request):
    if request.user.user_type != 'recipient':
        messages.error(request, 'Only recipients can access this dashboard.')
        return redirect('donor_dashboard')
    return render(request, 'recipient_dashboard.html')


def home(request):
    return render(request, 'home.html')
