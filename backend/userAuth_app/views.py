from userAuth_app.models import User
from userAuth_app.serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Agent, KeycloakUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.http import JsonResponse
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import KeycloakUser
from rest_framework.permissions import AllowAny
from .models import Agent
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import KeycloakUser




# Define the schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Your Omega API",
        default_version='v1',
        description="API documentation for Your Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
token_param_config = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Token [Authorization: Token <token>]",
    type=openapi.TYPE_STRING,
)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def save_keycloak_user(request):
    try:
        # Extract nested data from 'A1' and 'A2'
        user_data = request.data.get('A1')
        token_data = request.data.get('A2')
        print("user_data", user_data)
        print("token_data", token_data)


        # Ensure that 'A1' and 'A2' data exist
        if not user_data or not token_data:
            return Response({"error": "Invalid data structure: 'A1' and 'A2' are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure that required fields in 'A1' are present
        required_fields = ['id', 'userName', 'email']
        for field in required_fields:
            if field not in user_data:
                return Response({"error": f"Missing required field in 'A1': {field}"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure that 'value' exists in 'A2' data
        if 'value' not in token_data:
            return Response({"error": "Missing required field in 'A2': 'value'"}, status=status.HTTP_400_BAD_REQUEST)

        # Process the data (assuming KeycloakUser model)
        user, created = KeycloakUser.objects.update_or_create(
            keycloak_id=user_data['id'],
            # print("keycloak_id :", keycloak_id),
            defaults={
                'username': user_data['userName'],
                'access_token': token_data['value'],
                'email': user_data['email'],
                'nickname': user_data.get('nickname', 'N/A'),
                # 'roles': user_data.get('roles', []),
                'roles': json.dumps(user_data.get('roles', []))  # Convert list to JSON string

            }
        )
        print("User saved:", user)

        return Response({
            "message": "User saved successfully" if created else "User updated successfully",
            "user_id": user.id,
            "created": created,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserListAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # Use custom permission classes
    def get(self, request):
        # Fetch all users from KeycloakUser model
        users = KeycloakUser.objects.all()
        # Prepare data to return
        user_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "nickname": user.nickname,
                "roles": user.roles,
            }
            for user in users
        ]
        return Response(user_data)


 
@permission_classes([AllowAny]) 
class AgentAPIView(APIView):
    def get(self, request, pk=None):
        """
        Handle GET requests. If `pk` is provided, return a single Agent. Otherwise, return all Agents.
        """
        if pk:
            agent = get_object_or_404(Agent, pk=pk)
            serializer = AgentSerializer(agent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def post(self, request):
        """
        Handle POST requests to create a new Agent.
        """
        data = request.data
        print("data",data)
        keycloak_id = data.get('keycloak_id')
        print("keycloak_id",keycloak_id)

        keycloak_user = get_object_or_404(KeycloakUser, keycloak_id=keycloak_id)
        data['keycloak_user'] = keycloak_user.id  # Replace keycloak_id with the actual user ID
        serializer = AgentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Agent.
        """
        agent = get_object_or_404(Agent, pk=pk)
        data = request.data
        keycloak_id = data.get('keycloak_id')
        if keycloak_id:
            keycloak_user = get_object_or_404(KeycloakUser, keycloak_id=keycloak_id)
            data['keycloak_user'] = keycloak_user.id  # Replace keycloak_id with the actual user ID
        serializer = AgentSerializer(agent, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete an Agent.
        """
        agent = get_object_or_404(Agent, pk=pk)
        agent.delete()
        return Response({'message': 'Agent deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
 



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
    return response.json().get("keycloak_id")


# API view to create a new user in Keycloak
@csrf_exempt
def create_keycloak_user(request):
    if request.method == "POST":
        # Get the admin token from Keycloak
        K_id = get_admin_token()  
        print("get id :", K_id)
        
        # Set the headers for authentication
        headers = {"Authorization": f"Bearer {K_id}", "Content-Type": "application/json"}
        
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





class UserRegistrationView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    @swagger_auto_schema(
        operation_description="User registration",
        request_body=UserSerializer,
        manual_parameters=[token_param_config],
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        print(username)
        password = request.data.get('password')
        print(f'{username} and {password}')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            return Response({'token': token.key, 'username': user.username, 'role': user.role})
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        # Access the authenticated user
        print("logout trigger")
        user = request.user
        print("User:", user.username)  # Print the username
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        print(token)
        token.delete()
        return Response({'detail': 'Successfully logged out.'})
