from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField, EmailField


class UserProfileRetrieveSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]


class UserProfileCreateUpdateSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True, max_length=64,)
    repeat_password = CharField(write_only=True, required=True, max_length=64,)

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
            'repeat_password',
            'first_name',
            'last_name',
        ]

    def validate(self, validated_data):
        if 'password' in validated_data or 'repeat_password' in validated_data:
            if validated_data['password'] != validated_data['repeat_password']:
                raise ValidationError("Password doesn't match repeat password.")
            validate_password(validated_data['password'])
        return validated_data

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        password = validated_data.pop('password')
        user = super(UserProfileCreateUpdateSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        validated_data.pop('email', None)
        validated_data.pop('repeat_password', None)
        password = validated_data.pop('password', None)
        instance = super(UserProfileCreateUpdateSerializer, self).update(instance, validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserProfileAuthSerializer(ModelSerializer):
    email = EmailField(write_only=True, required=True, max_length=64,)
    password = CharField(write_only=True, required=True, max_length=64,)

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
        ]

    def validate(self, validated_data):
        validate_password(validated_data['password'])
        user = authenticate(
            email=validated_data['email'],
            password=validated_data['password']
        )
        if not user:
            raise ValidationError("Wrong email or password.")
        validated_data['user'] = user
        return validated_data


class UserProfileRetrieveUpdateSerializer(ModelSerializer):
    email = EmailField(read_only=True, max_length=64,)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]
