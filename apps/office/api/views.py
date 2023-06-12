from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

from utils.api.permissions import IsCompanyOwnerOrReadOnly, IsUserACompanyOwner
from apps.office.api.serializers import OfficeListCreateSerializer, OfficeRetrieveUpdateDestroySerializer
from apps.office.models import Office


class OfficeListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsCompanyOwnerOrReadOnly,)
    serializer_class = OfficeListCreateSerializer

    filterset_fields = [
        'country',
        'city'
    ]

    def get_queryset(self):
        if self.request.user.company is None:
            return Office.objects.filter(company=self.request.user.owned_company)
        return Office.objects.filter(company=self.request.user.company)


class OfficeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsUserACompanyOwner,)
    serializer_class = OfficeRetrieveUpdateDestroySerializer

    def get_queryset(self):
        return Office.objects.filter(company=self.request.user.owned_company)


class OfficeWorkerRetrieveAPIView(RetrieveAPIView):
    serializer_class = OfficeRetrieveUpdateDestroySerializer

    def get_object(self, *args, **kwargs):
        return self.request.user.office
