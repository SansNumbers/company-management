from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField, ForeignKey, SET_NULL


class UserProfile(AbstractUser):
    username = None
    email = EmailField(
        verbose_name='email address',
        max_length=150,
        unique=True,
    )
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)

    company = ForeignKey(
        'company.Company',
        related_name='workers',
        on_delete=SET_NULL,
        null=True,
    )

    office = ForeignKey(
        'office.Office',
        related_name='workers',
        on_delete=SET_NULL,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
