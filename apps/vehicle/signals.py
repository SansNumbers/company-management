from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer

from apps.vehicle.models import Vehicle
from apps.vehicle.tasks import create_vehicle_audit


@receiver(post_save, sender=Vehicle)
def broadcast_report(sender, instance, created, **kwargs):
    if created:
        async_to_sync(get_channel_layer().group_send)(
            f'vehicles_{instance.company.pk}',
            {
                'type': 'send_vehicle',
                'text': instance.name
            }
        )


@receiver(post_save, sender=Vehicle)
def create_audit(sender, instance, created, **kwargs):
    create_vehicle_audit.delay(instance.pk)
