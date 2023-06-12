from django.urls import path, include

from apps.vehicle.api import views

urlpatterns = [
    path('vehicles/', views.VehicleListCreateAPIView.as_view()),
    path('vehicles/<int:pk>/', views.VehicleRetrieveUpdateDestroyAPIView.as_view()),
    path('vehicles/my/', views.DriverVehiclesListAPIView.as_view()),
    path('vehicles/', include('apps.audit.api.urls')),
]
