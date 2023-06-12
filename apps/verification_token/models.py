import binascii
import os

from django.conf import settings
from django.db.models import Model, CharField, CASCADE, OneToOneField, DateTimeField
from django.utils.translation import gettext_lazy as _


class VerificationToken(Model):
    key = CharField(_("Key"), max_length=40, primary_key=True)
    user = OneToOneField(
        settings.AUTH_USER_MODEL, related_name='verification_token',
        on_delete=CASCADE, verbose_name=_("User")
    )
    created = DateTimeField(_("Created"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
