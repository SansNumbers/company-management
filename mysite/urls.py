from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('apps.poll.urls')),
    path('member/', include('django.contrib.auth.urls')),
    path('member/', include('apps.member.urls')),
    path('worker/', include('apps.worker.urls')),
    path('vehicle/', include('apps.vehicle.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.user_profile.api.urls')),
    path('api/v1/', include('apps.company.api.urls')),
    path('api/v1/', include('apps.worker.api.urls')),
    path('api/v1/', include('apps.office.api.urls')),
    path('api/v1/', include('apps.vehicle.api.urls')),
]
