from django.urls import path

from apps.vehicle import views

urlpatterns = [
    path('', views.Vehicles.as_view())
]
