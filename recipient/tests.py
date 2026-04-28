from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import BloodRequest


class RecipientRequestTests(TestCase):
    def setUp(self):
        self.recipient = CustomUser.objects.create_user(
            username='recipient',
            password='pass12345',
            user_type='recipient',
            phone='3333333333',
            city='Austin',
        )
        self.donor = CustomUser.objects.create_user(
            username='donor',
            password='pass12345',
            user_type='donor',
            phone='4444444444',
            city='Dallas',
        )

    def test_recipient_can_create_valid_request(self):
        self.client.force_login(self.recipient)

        response = self.client.post(
            reverse('request_blood'),
            {'blood_group': 'A+', 'units': '2', 'city': 'Austin'},
        )

        self.assertRedirects(response, reverse('request_status'))
        self.assertEqual(BloodRequest.objects.count(), 1)

    def test_invalid_units_are_rejected(self):
        self.client.force_login(self.recipient)

        response = self.client.post(
            reverse('request_blood'),
            {'blood_group': 'A+', 'units': '0', 'city': 'Austin'},
            follow=True,
        )

        self.assertEqual(BloodRequest.objects.count(), 0)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Please provide valid blood group, city, and units.', messages)

    def test_donor_cannot_open_request_pages(self):
        self.client.force_login(self.donor)

        response = self.client.get(reverse('request_status'))

        self.assertRedirects(response, reverse('donor_dashboard'))
