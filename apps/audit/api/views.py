import json
import os

import requests
from django.core.serializers import serialize
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.audit.api.serializers import AuditListSerializer
from apps.audit.models import Audit
from utils.api.permissions import IsUserACompanyOwner


class AuditListAPIView(ListAPIView):
    permission_classes = (IsUserACompanyOwner, )
    serializer_class = AuditListSerializer

    def get_queryset(self):
        return Audit.objects.filter(
            company=self.request.user.owned_company
        ).filter(
            created_on__range=[self.request.query_params.get('start_date'), self.request.query_params.get('end_date')]
        )

    def get(self, request, *args, **kwargs):
        audits_queryset = self.get_queryset()
        serialized_data = serialize("json", audits_queryset)
        serialized_data = json.loads(serialized_data)
        flask_response = requests.get(
            f'http://{os.environ.get("FLASK_URL_DOMAIN")}:{os.environ.get("FLASK_URL_PORT")}/',
            data=bytes(str(serialized_data), 'UTF-8'),
            headers={
                "Auth-sync": os.environ.get('SECRET_SYNC_KEY'),
            },
        )
        json_flask_response = flask_response.content.decode('utf8').replace("'", '"')
        return Response(json.loads(json_flask_response), status=HTTP_200_OK)
