from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_registration_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Your Free Account")

    def test_registration_success(self):
        data = {
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertTrue(User.objects.filter(username='john_doe').exists())

    def test_registration_password_mismatch(self):
        data = {
            'username': 'mismatch_user',
            'first_name': 'Mismatch',
            'last_name': 'User',
            'email': 'mismatch@example.com',
            'password': 'password123',
            'confirm_password': 'wrongpassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatch_user').exists())
        self.assertContains(response, "Passwords do not match")

    def test_login_and_logout(self):
        user = User.objects.create_user(username='tester', password='testpassword123')
        # Login
        response = self.client.post(self.login_url, {
            'username': 'tester',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        # Logout
        logout_response = self.client.get(self.logout_url)
        self.assertEqual(logout_response.status_code, 302)
