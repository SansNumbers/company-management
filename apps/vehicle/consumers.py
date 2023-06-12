import json

from channels.generic.websocket import AsyncWebsocketConsumer

from apps.vehicle.api.serializers import VehicleListCreateSerializer
from apps.vehicle.models import Vehicle


class VehicleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(f'vehicles_{self.scope["user"].owned_company.pk}', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(f'vehicles_{self.scope["user"].owned_company.pk}', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data = int(text_data)
        except (ValueError, TypeError):
            await self.send(text_data=json.dumps({
                'error': 'Error has occured.'
            }))
        vehicles = Vehicle.objects.filter(office_id=text_data)
        serializer = VehicleListCreateSerializer(vehicles, many=True)
        await self.send(text_data=json.dumps(serializer.data))

    async def send_vehicle(self, event):
        await self.send(text_data=json.dumps({
            'receive_vehicle': event['text']
        }))
