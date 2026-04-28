from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import CustomUser


# 🔹 REGISTER VIEW
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']

        # check if user already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # create user
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            user_type=user_type
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')


# 🔹 LOGIN VIEW
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # redirect based on user type
            if user.user_type.lower() == 'donor':
                return redirect('donor_dashboard')
            else:
                return redirect('recipient_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# 🔹 DONOR DASHBOARD
def donor_dashboard(request):
    return render(request, 'donor_dashboard.html')


# 🔹 RECIPIENT DASHBOARD
def recipient_dashboard(request):
    return render(request, 'recipient_dashboard.html')

def home(request):
    return render(request, 'home.html')