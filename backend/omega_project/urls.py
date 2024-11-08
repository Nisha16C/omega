# project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path # Import the include function
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions




schema_view = get_schema_view(
    openapi.Info(
        title="Your OMEGA API",
        default_version='v1',
        description="API documentation for Your Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("api/v1/", include('userAuth_app.urls')),
    path("api/v6/", include('keycloak_app.urls')),



    path('admin/', admin.site.urls),
    path("api/v3/", include('rule__api.urls')),  # Include your app's URLs here
    path("", include('userAuth_app.urls')),  # Include your app's URLs here
    path("api/v5/", include('ADSapp.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



