from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import RegistrationForm, LoginForm, CustomPasswordChangeForm

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_view(self):
        # Test GET request
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Test POST request with valid credentials
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(response.wsgi_request.user, self.user)
    
    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Invalid credentials')

    def test_register_view(self):
        # Test GET request
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        # Test POST request with valid data
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'Passwords do not match.')

    def test_change_password_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

        # Test POST request with valid data
        response = self.client.post(reverse('change-password'), {
            'old_password': self.password,
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        self.assertRedirects(response, reverse('index'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword456'))

    def test_change_password_view_incorrect_old_password(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('change-password'), {
            'old_password': 'wrongoldpassword',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'old_password', 'Current password is incorrect')

