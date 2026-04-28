from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class AuthFlowTests(TestCase):
    def test_register_rejects_invalid_user_type(self):
        response = self.client.post(
            reverse('register'),
            {'username': 'baduser', 'password': 'pw12345', 'user_type': 'admin'},
            follow=True,
        )

        self.assertFalse(CustomUser.objects.filter(username='baduser').exists())
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Please provide a valid username, password, and user type.', messages)

    def test_login_redirects_donor_to_donor_dashboard(self):
        CustomUser.objects.create_user(
            username='donor1',
            password='pass12345',
            user_type='donor',
            phone='1111111111',
            city='NYC',
        )

        response = self.client.post(
            reverse('login'),
            {'username': 'donor1', 'password': 'pass12345'},
        )

        self.assertRedirects(response, reverse('donor_dashboard'))

    def test_dashboard_blocks_wrong_role(self):
        user = CustomUser.objects.create_user(
            username='recipient1',
            password='pass12345',
            user_type='recipient',
            phone='2222222222',
            city='Boston',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('donor_dashboard'))

        self.assertRedirects(response, reverse('recipient_dashboard'))
