from django.shortcuts import render
from django.db.models import Sum

from .models import BloodInventory


def inventory_list(request):
    blood_group = request.GET.get('blood_group', '').strip().upper()

    data = BloodInventory.objects.all().order_by('blood_group')
    if blood_group:
        data = data.filter(blood_group__iexact=blood_group)

    all_inventory = BloodInventory.objects.all().order_by('blood_group')
    context = {
        'data': data,
        'selected_blood_group': blood_group,
        'all_blood_groups': [item.blood_group for item in all_inventory],
        'total_units': all_inventory.aggregate(total=Sum('units_available'))['total'] or 0,
        'low_stock_count': all_inventory.filter(units_available__lt=6).count(),
    }
    return render(request, 'inventory.html', context)
