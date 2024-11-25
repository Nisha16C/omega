# middleware.py
from django.http import JsonResponse
from userAuth_app.models import KeycloakUser  # Replace with your User model path

class KeycloakIDAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        keycloak_id = request.headers.get("Keycloak-ID")

        if not keycloak_id or not KeycloakUser.objects.filter(keycloak_id=keycloak_id).exists():
            return JsonResponse({'error': 'Authentication failed. Invalid Keycloak-ID.'}, status=401)

        # Attach the user to the request
        request.username = KeycloakUser.objects.get(keycloak_id=keycloak_id)
        response = self.get_response(request)
        return response
