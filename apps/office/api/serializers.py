from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.office.models import Office


class OfficeListCreateSerializer(ModelSerializer):
    class Meta:
        model = Office
        fields = [
            'id',
            'name',
            'address',
            'country',
            'city',
            'region',
            'workers',
            'vehicles',
            'vehicle_count'
        ]
        extra_kwargs = {
            'workers': {'required': False},
            'vehicles': {'required': False},
        }

    def create(self, validated_data):
        validated_data['company'] = self.context['request'].user.owned_company
        office = super(OfficeListCreateSerializer, self).create(validated_data)
        office.save()
        return office


class OfficeRetrieveUpdateDestroySerializer(ModelSerializer):
    class Meta:
        model = Office
        fields = [
            'id',
            'name',
            'address',
            'country',
            'city',
            'region',
            'workers',
            'vehicles',
            'vehicle_count'
        ]
        extra_kwargs = {
            'workers': {'required': False},
            'vehicles': {'required': False},
        }

    def validate(self, validated_data):
        workers = validated_data.get('workers', None)
        vehicles = validated_data.get('vehicles', None)
        if workers is not None or vehicles is not None:
            validated_data = self.validate_workers_and_vehicles(workers, vehicles, validated_data)
        return validated_data

    def validate_workers_and_vehicles(self, workers, vehicles, validated_data):
        if vehicles is None:
            validated_data['vehicles'] = []
            if workers is not None:
                for worker in workers:
                    worker.vehicle_set.set([])
                return validated_data

        if workers is None:
            validated_data['workers'] = []
            if vehicles is not None:
                for vehicle in vehicles:
                    vehicle.drivers.set([])
                return validated_data

        if vehicles is not None and workers is not None:
            for vehicle in vehicles:
                if self.instance.id != vehicle.office_id:
                    raise ValidationError(f"Vehicle {vehicle.id} already belongs to office {vehicle.office_id}")
            for worker in workers:
                if self.instance.id != worker.office_id:
                    if worker.office_id is None:
                        raise ValidationError("User is a company owner")
                    raise ValidationError(f"Worker {worker.id} already belongs to office {worker.office_id}")
            return validated_data
