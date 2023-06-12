from django.db.models import Model, SET_NULL, DateTimeField, ForeignKey, ManyToManyField, CASCADE


class Audit(Model):
    vehicle = ForeignKey(
        'vehicle.Vehicle',
        related_name='audit',
        on_delete=SET_NULL,
        null=True,
    )
    drivers = ManyToManyField(
        'user_profile.UserProfile',
        related_query_name='drivers',
        blank=True
    )
    office = ForeignKey(
        'office.Office',
        related_name='office',
        on_delete=SET_NULL,
        null=True,
    )
    company = ForeignKey(
        'company.Company',
        related_name='audits',
        on_delete=CASCADE,
    )
    created_on = DateTimeField(auto_now_add=True)
