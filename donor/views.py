from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Donor


@login_required
def donate_blood(request):
    if request.user.user_type != 'donor':
        messages.error(request, 'Only donor accounts can access the donation page.')
        if request.user.user_type == 'recipient':
            return redirect('recipient_dashboard')
        return redirect('home')

    donor_profile = Donor.objects.filter(user=request.user).first()

    if request.method == 'POST':
        blood_group = request.POST.get('blood_group', '').strip()
        last_donation_date = request.POST.get('last_donation_date', '').strip() or None

        if blood_group not in {'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'}:
            messages.error(request, 'Please choose a valid blood group before saving.')
            return redirect('donate_blood')

        donor_profile, created = Donor.objects.update_or_create(
            user=request.user,
            defaults={
                'blood_group': blood_group,
                'last_donation_date': last_donation_date,
            },
        )

        if created:
            messages.success(request, 'Your donor profile has been created and you are marked ready to donate.')
        else:
            messages.success(request, 'Your donor details have been updated successfully.')
        return redirect('donor_dashboard')

    context = {
        'blood_groups': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'donor_profile': donor_profile,
    }
    return render(request, 'donate_blood.html', context)
