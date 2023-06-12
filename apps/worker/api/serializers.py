from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer


class WorkerListCreateSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True, max_length=64,)
    repeat_password = CharField(write_only=True, required=True, max_length=64,)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'password',
            'repeat_password',
            'first_name',
            'last_name',
            'office',
            'vehicle_set',
        ]
        extra_kwargs = {
            'office': {'required': False},
            'vehicle_set': {'required': False},
        }

    def validate(self, validated_data):
        if 'password' in validated_data or 'repeat_password' in validated_data:
            if validated_data['password'] != validated_data['repeat_password']:
                raise ValidationError("Password doesn't match repeat password.")
            validate_password(validated_data['password'])
        return validated_data

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        password = validated_data.pop('password')
        validated_data['company'] = self.context['request'].user.owned_company
        worker = super(WorkerListCreateSerializer, self).create(validated_data)
        worker.set_password(password)
        worker.is_active = False
        worker.save()
        return worker


class WorkerRetrieveUpdateDestroySerializer(ModelSerializer):
    password = CharField(write_only=True, required=True, max_length=64,)
    repeat_password = CharField(write_only=True, required=True, max_length=64,)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'password',
            'repeat_password',
            'first_name',
            'last_name',
            'office',
            'vehicle_set',
        ]
        extra_kwargs = {
            'office': {'required': False},
            'vehicle_set': {'required': False},
        }

    def validate(self, validated_data):
        if 'password' in validated_data or 'repeat_password' in validated_data:
            if validated_data['password'] != validated_data['repeat_password']:
                raise ValidationError("Password doesn't match repeat password.")
            validate_password(validated_data['password'])
        office = False
        if 'office' in validated_data:
            office = validated_data['office']
        vehicles = validated_data.get('vehicle_set', None)
        if office is not False or vehicles is not None:
            validated_data = self.validate_office_and_vehicles(office, vehicles, validated_data)
        return validated_data

    def validate_office_and_vehicles(self, office, vehicles, validated_data):
        if office is None:
            validated_data['vehicle_set'] = []
            return validated_data

        if office is False:
            for vehicle in vehicles:
                if vehicle.office != self.instance.office_id:
                    raise ValidationError(f"Vehicle {vehicle.id} doesn't belong to office {self.instance.office_id}")
            return validated_data

        if office is not False:
            if vehicles is None:
                validated_data['vehicle_set'] = []
                return validated_data
            for vehicle in vehicles:
                if vehicle.office_id != office.id:
                    raise ValidationError(
                        f"Vehicle {vehicle.id} doesn't belong to office {office.id}")
            return validated_data

    def update(self, instance, validated_data):
        validated_data.pop('email', None)
        validated_data.pop('repeat_password', None)
        password = validated_data.pop('password', None)
        instance = super(WorkerRetrieveUpdateDestroySerializer, self).update(instance, validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
