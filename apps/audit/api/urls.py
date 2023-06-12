from django.urls import path

from apps.audit.api import views

urlpatterns = [
    path('audit/', views.AuditListAPIView.as_view(), name='audit'),
]
