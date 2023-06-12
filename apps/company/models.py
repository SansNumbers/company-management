from django.db.models import Model, CharField, OneToOneField, CASCADE


class Company(Model):
    name = CharField(max_length=64, unique=True)
    address = CharField(max_length=256,)
    owner = OneToOneField(
        'user_profile.UserProfile',
        related_name='owned_company',
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.name
