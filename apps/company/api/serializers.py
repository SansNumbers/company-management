from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer, HiddenField

from apps.company.models import Company


class CompanyCreateRetrieveUpdateSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Company
        fields = '__all__'
