from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from utils.api.permissions import IsCompanyOwnerOrReadOnly, IsUserACompanyOwner
from apps.vehicle.api.serializers import VehicleListCreateSerializer, VehicleRetrieveUpdateDestroySerializer
from apps.vehicle.models import Vehicle


class VehicleListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsCompanyOwnerOrReadOnly,)
    serializer_class = VehicleListCreateSerializer

    filterset_fields = [
        'office',
        'drivers',
    ]

    def get_queryset(self):
        if self.request.user.company is None:
            return Vehicle.objects.filter(company=self.request.user.owned_company)
        return Vehicle.objects.filter(company=self.request.user.company)


class DriverVehiclesListAPIView(ListAPIView):
    serializer_class = VehicleListCreateSerializer

    def get_queryset(self):
        return self.request.user.vehicle_set.all()


class VehicleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsUserACompanyOwner,)
    serializer_class = VehicleRetrieveUpdateDestroySerializer

    def get_queryset(self):
        return Vehicle.objects.filter(company=self.request.user.owned_company)
