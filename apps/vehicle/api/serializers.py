from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.vehicle.models import Vehicle


class VehicleListCreateSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'name',
            'licence_plate',
            'model',
            'year_of_manufacture',
            'office',
            'drivers',
        ]
        extra_kwargs = {
            'office': {'required': False},
            'drivers': {'required': False},
        }

    def create(self, validated_data):
        validated_data['company'] = self.context['request'].user.owned_company
        vehicle = super(VehicleListCreateSerializer, self).create(validated_data)
        vehicle.save()
        return vehicle


class VehicleRetrieveUpdateDestroySerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'name',
            'licence_plate',
            'model',
            'year_of_manufacture',
            'office',
            'drivers',
        ]
        extra_kwargs = {
            'office': {'required': False},
            'drivers': {'required': False},
        }

    def validate(self, validated_data):
        office = False
        if 'office' in validated_data:
            office = validated_data['office']
        drivers = validated_data.get('drivers', None)
        if office is not False or drivers is not None:
            validated_data = self.validate_office_and_drivers(office, drivers, validated_data)
        return validated_data

    def validate_office_and_drivers(self, office, drivers, validated_data):
        if office is None:
            validated_data['drivers'] = []
            return validated_data

        if office is False:
            for driver in drivers:
                if driver.office != self.instance.office_id:
                    raise ValidationError(f"Driver {driver.id} doesn't belong to office {self.instance.office_id}")
            return validated_data

        if office is not False:
            if drivers is None:
                validated_data['drivers'] = []
                return validated_data
            for driver in drivers:
                if driver.office_id != office.id:
                    raise ValidationError(
                        f"Driver {driver.id} doesn't belong to office {office.id}")
            return validated_data
