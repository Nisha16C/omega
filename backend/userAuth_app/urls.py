# multi_role_auth/urls.py

from django.urls import path, include, re_path
from userAuth_app.views import *
from .views import schema_view
from . import views


urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('save-keycloak-user/', views.save_keycloak_user, name='save_keycloak_user'),
    path('agents/', AgentAPIView.as_view(), name='agent_list_create'),  # List & Create
    path('agents/<int:pk>/', AgentAPIView.as_view(), name='agent_detail'),  # Retrieve, Update & Delete
    path('users/', UserListAPIView.as_view(), name='user_list'),
    path('create-keycloak-user/', views.create_keycloak_user, name='create_keycloak_user'),
    path('update-user/', UpdateKeycloakUserAPIView.as_view(), name='update-keycloak-user'),


]


    