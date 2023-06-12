from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from utils.api.permissions import IsCompanyOwnerOrReadOnly, IsNotACompanyOwnerOrWorker
from apps.company.api.serializers import CompanyCreateRetrieveUpdateSerializer
from apps.company.models import Company


class CompanyCreateAPIView(CreateAPIView):
    permission_classes = (IsNotACompanyOwnerOrWorker, )
    serializer_class = CompanyCreateRetrieveUpdateSerializer


class CompanyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsCompanyOwnerOrReadOnly, )
    serializer_class = CompanyCreateRetrieveUpdateSerializer

    def get_queryset(self):
        if self.request.user.company is None:
            return Company.objects.filter(owner=self.request.user)
        return Company.objects.filter(pk=self.request.user.company.pk)
