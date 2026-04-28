from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import Donor


class DonorFlowTests(TestCase):
    def setUp(self):
        self.donor = CustomUser.objects.create_user(
            username='donor1',
            password='pass12345',
            user_type='donor',
            phone='1111111111',
            city='Delhi',
        )
        self.recipient = CustomUser.objects.create_user(
            username='recipient1',
            password='pass12345',
            user_type='recipient',
            phone='2222222222',
            city='Mumbai',
        )

    def test_donor_can_save_donation_profile(self):
        self.client.force_login(self.donor)

        response = self.client.post(
            reverse('donate_blood'),
            {'blood_group': 'O+', 'last_donation_date': '2026-04-01'},
        )

        self.assertRedirects(response, reverse('donor_dashboard'))
        donor_profile = Donor.objects.get(user=self.donor)
        self.assertEqual(donor_profile.blood_group, 'O+')

    def test_recipient_cannot_access_donate_page(self):
        self.client.force_login(self.recipient)

        response = self.client.get(reverse('donate_blood'))

        self.assertRedirects(response, reverse('recipient_dashboard'))
