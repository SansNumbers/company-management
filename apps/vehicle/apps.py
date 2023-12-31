from django.apps import AppConfig


class VehicleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.vehicle'

    def ready(self):
        import apps.vehicle.signals
