from django.urls import path

from apps.company.api import views

urlpatterns = [
    path('companies/', views.CompanyCreateAPIView.as_view(), name='companies'),
    path('companies/<int:pk>/', views.CompanyRetrieveUpdateAPIView.as_view(), name='company'),
]
