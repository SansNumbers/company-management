from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.worker.tasks import send_verification_email_task


@receiver(post_save, sender=get_user_model())
def send_mail(sender, instance, created, **kwargs):
    if created:
        send_verification_email_task.delay(instance.pk)
