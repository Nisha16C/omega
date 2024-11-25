# your_app_name/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from omega_project.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def get(self, request):
        # request.user will have the username and roles if authentication is successful
        user_info = request.user
        username = user_info.get('username')
        roles = user_info.get('roles')
        return Response({
            "message": "Token is valid",
            "username": username,
            "roles": roles
        }, status=200)

def get_admin_token():
    url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "client_id": "omega-admin",
        "grant_type": "password",
        "username": "admin",  # Replace with your Keycloak admin username
        "password": "admin"   # Replace with your Keycloak admin password
    }
    print("get data :", data)
    response = requests.post(url, data=data)
    return response.json().get("access_token")

# API view to create a new user in Keycloak
@csrf_exempt
def create_keycloak_user(request):
    if request.method == "POST":
        # Get the admin token from Keycloak
        token = get_admin_token()  
        print("get token :", token)
        # Set the headers for authentication
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        # Parse the JSON data from the request body
        try:
            data = json.loads(request.body)  # Correct way to parse incoming JSON data
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        # Prepare the payload for the new user creation
        user_payload = {
            "username": data.get("username"),
            "email": data.get("email"),
            "firstName": data.get("firstName", "DefaultFirstName"),  # Optional field: Add first name
            "lastName": data.get("lastName", "DefaultLastName"),  # Optional field: Add last name
            "enabled": True,
            "credentials": [{
                "type": "password",
                "value": data.get("password"),
                "temporary": False  # Set to False if you do not want the password to be temporary
            }]
        }
        print("user_payload :", user_payload)
        # Make the request to Keycloak's user creation endpoint
        response = requests.post(
            f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users",
            headers=headers,
            json=user_payload  # Send the payload as JSON
        )
        print("response :", response)
        # Check the response status code and return appropriate response
        if response.status_code == 201:
            return JsonResponse({"message": "User created successfully in Keycloak"}, status=201)
        else:
            # Print response for debugging
            print("Error response:", response.text)
            return JsonResponse({"error": "Failed to create user", "details": response.text}, status=response.status_code)
