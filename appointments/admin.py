from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_datetime', 'status', 'created_at')
    list_filter = ('status', 'appointment_datetime', 'created_at')
    search_fields = ('patient__username', 'doctor__username')
    date_hierarchy = 'appointment_datetime'