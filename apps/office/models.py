from django.db.models import Model, CharField, ForeignKey, CASCADE, PositiveSmallIntegerField


class Office(Model):
    name = CharField(max_length=64,)
    address = CharField(max_length=256,)
    country = CharField(max_length=64,)
    city = CharField(max_length=64,)
    region = CharField(max_length=64,)

    company = ForeignKey(
        'company.Company',
        related_name='offices',
        on_delete=CASCADE,
    )

    vehicle_count = PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
