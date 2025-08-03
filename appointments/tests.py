from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Appointment

User = get_user_model()

class AppointmentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test users
        self.patient = User.objects.create_user(
            username='patient1',
            email='patient1@test.com',
            password='testpass123',
            role='patient'
        )
        
        self.doctor = User.objects.create_user(
            username='doctor1',
            email='doctor1@test.com',
            password='testpass123',
            role='doctor'
        )
        
        self.create_appointment_url = reverse('create_appointment')
        
    def test_create_appointment(self):
        """Test appointment creation by patient"""
        self.client.force_authenticate(user=self.patient)
        
        future_datetime = timezone.now() + timedelta(days=1)
        data = {
            'doctor': self.doctor.id,
            'appointment_datetime': future_datetime.isoformat(),
            'symptoms': 'Fever and headache'
        }
        
        response = self.client.post(self.create_appointment_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Appointment.objects.filter(patient=self.patient, doctor=self.doctor).exists())
        
    def test_appointment_list_for_patient(self):
        """Test appointment listing for patient"""
        # Create test appointment
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_datetime=timezone.now() + timedelta(days=1),
            symptoms='Test symptoms'
        )
        
        self