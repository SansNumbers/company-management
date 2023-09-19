from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Company Management API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
