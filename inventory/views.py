from django.shortcuts import render

from .models import BloodInventory


def inventory_list(request):
    blood_group = request.GET.get('blood_group', '').strip().upper()

    data = BloodInventory.objects.all().order_by('blood_group')
    if blood_group:
        data = data.filter(blood_group__iexact=blood_group)

    return render(request, 'inventory.html', {'data': data, 'selected_blood_group': blood_group})
