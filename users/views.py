import logging
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import User, DoctorProfile, PatientProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    UserSerializer, DoctorProfileSerializer, PatientProfileSerializer
)

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"New user registered: {user.username} as {user.role}")
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response({'error': 'Registration failed'}, 
                          status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    try:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        # Update online status
        user.is_online = True
        user.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"User logged in: {user.username}")
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response({'error': 'Login failed'}, 
                      status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    try:
        # Update online status
        request.user.is_online = False
        request.user.save()
        
        logger.info(f"User logged out: {request.user.username}")
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response({'error': 'Logout failed'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class DoctorListView(generics.ListAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(role='doctor', is_active=True)

class UpdateDoctorProfileView(generics.UpdateAPIView):
    serializer_class = DoctorProfileSerializer
    
    def get_object(self):
        doctor_profile, created = DoctorProfile.objects.get_or_create(
            user=self.request.user
        )
        return doctor_profile

class UpdatePatientProfileView(generics.UpdateAPIView):
    serializer_class = PatientProfileSerializer
    
    def get_object(self):
        patient_profile, created = PatientProfile.objects.get_or_create(
            user=self.request.user
        )
        return patient_profile