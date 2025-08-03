
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
    def test_user_registration(self):
        """Test user registration endpoint"""
        data = {
            'username': 'testpatient',
            'email': 'patient@test.com',
            'first_name': 'Test',
            'last_name': 'Patient',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'role': 'patient',
            'phone': '1234567890'
        }
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testpatient').exists())
        self.assertIn('tokens', response.data)
        
    def test_user_login(self):
        """Test user login endpoint"""
        # Create user first
        user = User.objects.create_user(
            username='testdoctor',
            email='doctor@test.com',
            password='testpass123',
            role='doctor'
        )
        
        data = {
            'username': 'testdoctor',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        
        # Check if user is marked as online
        user.refresh_from_db()
        self.assertTrue(user.is_online)