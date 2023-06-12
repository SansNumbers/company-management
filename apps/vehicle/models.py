from django.db.models import Model, CharField, ForeignKey, PositiveIntegerField, CASCADE, ManyToManyField, SET_NULL


class Vehicle(Model):
    name = CharField(max_length=64,)
    licence_plate = CharField(max_length=64,)
    model = CharField(max_length=64,)
    year_of_manufacture = PositiveIntegerField()

    company = ForeignKey(
        'company.Company',
        related_name='vehicles',
        on_delete=CASCADE,
    )

    office = ForeignKey(
        'office.Office',
        related_name='vehicles',
        on_delete=SET_NULL,
        null=True
    )

    drivers = ManyToManyField(
        'user_profile.UserProfile',
        related_query_name='vehicles',
    )
