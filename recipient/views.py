from django.shortcuts import render, redirect
from .models import BloodRequest


# 🩸 Request Blood
def request_blood(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        units = request.POST['units']
        city = request.POST['city']

        BloodRequest.objects.create(
            user=request.user,
            blood_group=blood_group,
            units=units,
            city=city
        )

        return redirect('request_status')

    return render(request, 'request_form.html')


# 📊 Request Status
def request_status(request):
    requests = BloodRequest.objects.filter(user=request.user)
    return render(request, 'request_status.html', {'requests': requests})