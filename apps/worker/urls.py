from django.urls import path

from apps.worker import views

urlpatterns = [
    path('email-verify/', views.WorkerActivateView.as_view(), name='activate-worker')
]
