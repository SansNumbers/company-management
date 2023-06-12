from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/socket-server/', consumers.VehicleConsumer.as_asgi())
]
