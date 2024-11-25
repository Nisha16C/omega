from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import KeycloakUser  # Replace with the actual path to your User model

class KeycloakIDPermission(BasePermission):
    """
    Custom permission to check if the request is authenticated using keycloak_id.
    """
    def has_permission(self, request, view):
        # Get the Keycloak ID from the request headers
        keycloak_id = request.headers.get("Keycloak-ID")
        
        if not keycloak_id:
            return False  # Deny access if no Keycloak-ID header is provided

        # Check if a user with this Keycloak ID exists
        user = KeycloakUser.objects.filter(keycloak_id=keycloak_id).first()
        print("new user ko print kro :", user)
        if not user:
            return False  # Deny access if user does not exist

        # Attach the user object to the request for further use
        request.username = user
        return True
