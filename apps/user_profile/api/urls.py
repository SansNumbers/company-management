from django.urls import path

from apps.user_profile.api import views

urlpatterns = [
    path('users/', views.UserProfileCreateAPIView.as_view(), name='register'),
    path('users/me/', views.UserProfileRetrieveUpdateAPIView.as_view(), name='profile'),
    path('auth/', views.UserProfileAuthAPIView.as_view(), name='auth'),
]
