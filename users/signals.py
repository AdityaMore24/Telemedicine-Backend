from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import User

@receiver(post_save, sender=User)
def user_status_changed(sender, instance, **kwargs):
    if instance.role == 'doctor':
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "doctors_status",
            {
                'type': 'doctor_status_update',
                'doctor': {
                    'id': instance.id,
                    'name': instance.get_full_name(),
                    'username': instance.username,
                    'is_online': instance.is_online,
                    'last_seen': instance.last_seen.isoformat() if instance.last_seen else None
                }
            }
        )