from rest_framework import serializers
from django.utils import timezone
from .models import Appointment
from users.serializers import UserSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient_details = UserSerializer(source='patient', read_only=True)
    doctor_details = UserSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_appointment_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Appointment cannot be scheduled in the past")
        return value
    
    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        if patient and patient.role != 'patient':
            raise serializers.ValidationError("Selected user is not a patient")
        if doctor and doctor.role != 'doctor':
            raise serializers.ValidationError("Selected user is not a doctor")
        
        return attrs

class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('doctor', 'appointment_datetime', 'symptoms')
    
    def validate_appointment_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Appointment cannot be scheduled in the past")
        return value
    
    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)