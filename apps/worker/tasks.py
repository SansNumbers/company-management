from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse

from apps.verification_token.models import VerificationToken
from apps.worker.api.utils import send_email


@shared_task
def send_verification_email_task(user_id):
    user = get_user_model().objects.get(pk=user_id)
    current_site = Site.objects.get_current()
    relativeLink = reverse('activate-worker')
    verification_token = VerificationToken.objects.create(user=user)
    absurl = f"http://{current_site}{relativeLink}?verification_token={verification_token}"
    email_body = f"Hi {user.first_name} \nUse link to verify your email \n{absurl}"
    send_email_data = {
        'email_body': email_body,
        'email_subject': 'Verify your email',
        'to_email': user.email,
    }
    send_email(send_email_data)
