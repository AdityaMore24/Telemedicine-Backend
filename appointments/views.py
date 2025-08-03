import logging
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Appointment
from .serializers import AppointmentSerializer, CreateAppointmentSerializer

logger = logging.getLogger(__name__)

class CreateAppointmentView(generics.CreateAPIView):
    serializer_class = CreateAppointmentSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            if request.user.role != 'patient':
                return Response({'error': 'Only patients can create appointments'}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            appointment = serializer.save()
            
            logger.info(f"Appointment created: {appointment.id}")
            
            return Response(AppointmentSerializer(appointment).data, 
                          status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Appointment creation error: {str(e)}")
            return Response({'error': 'Failed to create appointment'}, 
                          status=status.HTTP_400_BAD_REQUEST)

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        else:
            return Appointment.objects.filter(patient=user)

class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        else:
            return Appointment.objects.filter(patient=user)

@api_view(['PATCH'])
def update_appointment_status(request, appointment_id):
    try:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        # Only doctor can update status
        if request.user != appointment.doctor:
            return Response({'error': 'Only the assigned doctor can update status'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        appointment.status = new_status
        appointment.save()
        
        logger.info(f"Appointment {appointment_id} status updated to {new_status}")
        
        return Response(AppointmentSerializer(appointment).data)
    except Exception as e:
        logger.error(f"Status update error: {str(e)}")
        return Response({'error': 'Failed to update status'}, 
                      status=status.HTTP_400_BAD_REQUEST)