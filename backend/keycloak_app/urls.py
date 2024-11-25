# keycloak_app/urls.py

from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # path('token/', KeycloakTokenView.as_view(), name='keycloak_token'),
    # path('token/introspect/', KeycloakTokenIntrospectView.as_view(), name='keycloak_token_introspect'),
    # path('logout/', KeycloakLogoutView.as_view(), name='keycloak_logout'),
    path('protected/', ProtectedView.as_view(), name='ProtectedView'),
    path('create-keycloak-user/', views.create_keycloak_user, name='create_keycloak_user'),


]
