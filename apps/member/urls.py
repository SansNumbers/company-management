from django.urls import path

from apps.member import views

app_name = 'member'
urlpatterns = [
    path('login_user', views.LoginUser.as_view(), name='login'),
    path('logout_user', views.LogoutUser.as_view(), name='logout'),
    path('register_user', views.RegisterUser.as_view(), name='register'),
]
