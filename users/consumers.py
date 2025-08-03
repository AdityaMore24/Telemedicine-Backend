import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User

logger = logging.getLogger(__name__)

class DoctorStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("doctors_status", self.channel_name)
        await self.accept()
        
        # Send current doctor statuses
        doctors_status = await self.get_doctors_status()
        await self.send(text_data=json.dumps({
            'type': 'doctors_status',
            'doctors': doctors_status
        }))
        
        logger.info("WebSocket connected for doctor status updates")
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("doctors_status", self.channel_name)
        logger.info("WebSocket disconnected from doctor status updates")
    
    async def doctor_status_update(self, event):
        await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def get_doctors_status(self):
        doctors = User.objects.filter(role='doctor', is_active=True)
        return [
            {
                'id': doctor.id,
                'name': doctor.get_full_name(),
                'username': doctor.username,
                'is_online': doctor.is_online,
                'last_seen': doctor.last_seen.isoformat() if doctor.last_seen else None
            }
            for doctor in doctors
        ]