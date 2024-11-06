# keycloak_app/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # path('token/', KeycloakTokenView.as_view(), name='keycloak_token'),
    # path('token/introspect/', KeycloakTokenIntrospectView.as_view(), name='keycloak_token_introspect'),
    # path('logout/', KeycloakLogoutView.as_view(), name='keycloak_logout'),
    path('protected/', ProtectedView.as_view(), name='ProtectedView'),

]
