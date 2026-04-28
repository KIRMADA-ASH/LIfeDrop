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

    def test_invalid_user_type_does_not_loop_between_dashboards(self):
        user = CustomUser.objects.create_user(
            username='brokenuser',
            password='pass12345',
            user_type='recipient',
            phone='5555555555',
            city='Delhi',
        )
        user.user_type = ''
        user.save(update_fields=['user_type'])
        self.client.force_login(user)

        response = self.client.get(reverse('recipient_dashboard'))

        self.assertRedirects(response, reverse('home'))

    def test_logged_in_user_is_redirected_away_from_auth_pages(self):
        user = CustomUser.objects.create_user(
            username='donor2',
            password='pass12345',
            user_type='donor',
            phone='9999999999',
            city='Pune',
        )
        self.client.force_login(user)

        login_response = self.client.get(reverse('login'))
        register_response = self.client.get(reverse('register'))

        self.assertRedirects(login_response, reverse('donor_dashboard'))
        self.assertRedirects(register_response, reverse('donor_dashboard'))

    def test_home_hides_create_account_for_logged_in_recipient(self):
        user = CustomUser.objects.create_user(
            username='recipient2',
            password='pass12345',
            user_type='recipient',
            phone='8888888888',
            city='Chennai',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Request blood')
        self.assertNotContains(response, 'Create an account')
