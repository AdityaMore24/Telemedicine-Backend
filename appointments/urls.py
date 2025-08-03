from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateAppointmentView.as_view(), name='create_appointment'),
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:appointment_id>/status/', views.update_appointment_status, name='update_appointment_status'),
]