from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import KeycloakUser

class KeycloakIDAuthentication(BaseAuthentication):
   
    def authenticate(self, request):
        # Get the keycloak_id from the headers
        keycloak_id = request.headers.get('Keycloak-ID')
        print("keycloak_id :", keycloak_id)
        if not keycloak_id:
            return None  # No authentication header provided, proceed to next authentication class
        try:
            # Validate the keycloak_id against the database
            user = KeycloakUser.objects.get(keycloak_id=keycloak_id)
        except KeycloakUser.DoesNotExist:
            raise AuthenticationFailed("Invalid Keycloak ID")
        return (user, None)  # Return the user object and None for token
