from django.urls import path

from apps.office.api import views

urlpatterns = [
    path('offices/', views.OfficeListCreateAPIView.as_view()),
    path('offices/<int:pk>/', views.OfficeRetrieveUpdateDestroyAPIView.as_view()),
    path('offices/my/', views.OfficeWorkerRetrieveAPIView.as_view()),
]
