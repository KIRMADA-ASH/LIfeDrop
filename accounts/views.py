from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from .models import CustomUser
from inventory.models import BloodInventory
from recipient.models import BloodRequest


def _dashboard_name_for_user(user):
    if user.user_type == 'donor':
        return 'donor_dashboard'
    if user.user_type == 'recipient':
        return 'recipient_dashboard'
    return None


def home(request):
    inventory = BloodInventory.objects.all().order_by('blood_group')
    total_units = inventory.aggregate(total=Sum('units_available'))['total'] or 0
    active_requests = BloodRequest.objects.count()
    context = {
        'inventory_preview': inventory[:4],
        'total_units': total_units,
        'active_requests': active_requests,
        'donor_count': CustomUser.objects.filter(user_type='donor').count(),
        'recipient_count': CustomUser.objects.filter(user_type='recipient').count(),
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user_type = request.POST.get('user_type', '').strip()
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()

        if not username or not password or user_type not in {'donor', 'recipient'}:
            messages.error(request, 'Please provide a valid username, password, and user type.')
            return render(request, 'register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'That username is already taken.')
            return render(request, 'register.html')

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            user_type=user_type,
            phone=phone,
            city=city,
        )
        login(request, user)

        if user.user_type == 'donor':
            return redirect('donor_dashboard')
        return redirect('recipient_dashboard')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

        login(request, user)
        dashboard_name = _dashboard_name_for_user(user)
        if dashboard_name is None:
            logout(request)
            messages.error(request, 'Your account does not have a valid user type yet. Please register again or update this user in admin.')
            return redirect('login')
        return redirect(dashboard_name)

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def donor_dashboard(request):
    if request.user.user_type != 'donor':
        messages.error(request, 'This account is not a donor account.')
        dashboard_name = _dashboard_name_for_user(request.user)
        if dashboard_name is None:
            return redirect('home')
        return redirect(dashboard_name)

    inventory = BloodInventory.objects.all().order_by('blood_group')
    total_units = inventory.aggregate(total=Sum('units_available'))['total'] or 0
    low_stock = inventory.order_by('units_available', 'blood_group')[:3]
    context = {
        'total_units': total_units,
        'blood_group_count': inventory.count(),
        'recipient_count': CustomUser.objects.filter(user_type='recipient').count(),
        'pending_requests': BloodRequest.objects.filter(status='Pending').count(),
        'inventory_snapshot': inventory[:4],
        'low_stock_groups': low_stock,
    }
    return render(request, 'donor_dashboard.html', context)


@login_required
def recipient_dashboard(request):
    if request.user.user_type != 'recipient':
        messages.error(request, 'This account is not a recipient account.')
        dashboard_name = _dashboard_name_for_user(request.user)
        if dashboard_name is None:
            return redirect('home')
        return redirect(dashboard_name)

    requests = BloodRequest.objects.filter(user=request.user).order_by('-id')
    inventory = BloodInventory.objects.all().order_by('blood_group')
    context = {
        'request_count': requests.count(),
        'pending_count': requests.filter(status='Pending').count(),
        'approved_count': requests.filter(status='Approved').count(),
        'inventory_snapshot': inventory[:4],
        'recent_requests': requests[:3],
    }
    return render(request, 'recipient_dashboard.html', context)
