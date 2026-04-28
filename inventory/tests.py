from django.test import TestCase
from django.urls import reverse

from .models import BloodInventory


class InventoryTests(TestCase):
    def test_filter_is_case_insensitive(self):
        BloodInventory.objects.create(blood_group='A+', units_available=10)
        BloodInventory.objects.create(blood_group='B+', units_available=5)

        response = self.client.get(reverse('inventory'), {'blood_group': 'a+'})

        self.assertEqual(len(response.context['data']), 1)
        self.assertEqual(response.context['data'][0].blood_group, 'A+')
