from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.worker.api.serializers import WorkerListCreateSerializer, WorkerRetrieveUpdateDestroySerializer
from utils.api.permissions import IsUserACompanyOwner


class WorkerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsUserACompanyOwner,)
    serializer_class = WorkerListCreateSerializer

    filterset_fields = [
        'first_name',
        'last_name',
        'email'
    ]

    def get_queryset(self):
        return get_user_model().objects.filter(company=self.request.user.owned_company)


class WorkerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsUserACompanyOwner,)
    serializer_class = WorkerRetrieveUpdateDestroySerializer

    def get_queryset(self):
        return get_user_model().objects.filter(company=self.request.user.owned_company)


class WorkerVerifyEmailAPIView(GenericAPIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        worker = get_user_model().objects.filter(verification_token=request.query_params['verification_token']).last()
        if not worker or worker.verification_token.created < timezone.now() - timedelta(minutes=15):
            return Response({
                "message": f"Link is invalid. Please contact administrator."
            }, status=HTTP_400_BAD_REQUEST)
        if not worker.is_active:
            worker.is_active = True
            worker.save()
            worker.verification_token.delete()
        return Response({
            "message": f"You successfully confirmed your email. "
                       f"Please login http://{Site.objects.get_current()}{reverse('auth')}"
        }, status=HTTP_200_OK)
