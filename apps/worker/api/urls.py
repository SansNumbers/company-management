from django.urls import path

from apps.worker.api import views

urlpatterns = [
    path('workers/', views.WorkerListCreateAPIView.as_view(), name='workers'),
    path('workers/<int:pk>/', views.WorkerRetrieveUpdateDestroyAPIView.as_view(), name='worker'),
    path('workers/email-verify/', views.WorkerVerifyEmailAPIView.as_view(), name='email-verify')
]
