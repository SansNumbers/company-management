from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.company.models import Company


class IsNotACompanyOwnerOrWorker(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return not (request.user.company or Company.objects.filter(owner=request.user).exists())


class IsCompanyOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.company and request.method in SAFE_METHODS:
            return True
        try:
            request.user.owned_company
        except Company.DoesNotExist:
            return False
        return True


class IsUserACompanyOwner(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            request.user.owned_company
        except Company.DoesNotExist:
            return False
        return True
