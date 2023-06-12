from rest_framework.serializers import ModelSerializer

from apps.audit.models import Audit


class AuditListSerializer(ModelSerializer):
    class Meta:
        model = Audit
        fields = '__all__'
