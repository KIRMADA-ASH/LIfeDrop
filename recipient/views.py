from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import BloodRequest


@login_required
def request_blood(request):
    if request.user.user_type != 'recipient':
        messages.error(request, 'Only recipients can place blood requests.')
        return redirect('donor_dashboard')

    if request.method == 'POST':
        blood_group = request.POST.get('blood_group', '').strip()
        city = request.POST.get('city', '').strip()

        try:
            units = int(request.POST.get('units', 0))
        except (TypeError, ValueError):
            units = 0

        if not blood_group or not city or units <= 0:
            messages.error(request, 'Please provide valid blood group, city, and units.')
            return redirect('request_blood')

        BloodRequest.objects.create(
            user=request.user,
            blood_group=blood_group,
            units=units,
            city=city,
        )
        messages.success(request, 'Blood request submitted successfully.')
        return redirect('request_status')

    return render(
        request,
        'request_form.html',
        {
            'blood_groups': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        },
    )


@login_required
def request_status(request):
    if request.user.user_type != 'recipient':
        messages.error(request, 'Only recipients can view request status.')
        return redirect('donor_dashboard')

    requests = BloodRequest.objects.filter(user=request.user).order_by('-id')
    context = {
        'requests': requests,
        'pending_count': requests.filter(status='Pending').count(),
        'approved_count': requests.filter(status='Approved').count(),
        'rejected_count': requests.filter(status='Rejected').count(),
    }
    return render(request, 'request_status.html', context)
