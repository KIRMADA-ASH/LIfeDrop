from django.shortcuts import render
from .models import BloodInventory

def inventory_list(request):
    blood_group = request.GET.get('blood_group')

    if blood_group:
        data = BloodInventory.objects.filter(blood_group=blood_group)
    else:
        data = BloodInventory.objects.all()

    return render(request, 'inventory.html', {'data': data})