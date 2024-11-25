from userAuth_app.models import User
from userAuth_app.serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Agent, KeycloakUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
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


from .permissions import KeycloakIDPermission


@api_view(['GET'])
@permission_classes([AllowAny])
@permission_classes([KeycloakIDPermission])
def list_users(request):
    """
    API to list all users' information.
    Only accessible if the user is validated using the `keycloak_id`.
    """
    print("Inside list_users API - User validated with keycloak_id:", getattr(request, 'username', None))  # Print user from request after validation
    
    try:
        # Fetch all users from the database
        users = KeycloakUser.objects.all().values(
            'keycloak_id', 'username', 'email', 'nickname', 'roles'
        )
        print(f"Fetched {len(users)} users from the database.")  # Print number of users fetched
        return Response({"users": list(users)}, status=200)
    except Exception as e:
        print(f"Error fetching users: {str(e)}")  # Print error if something goes wrong
        return Response({"error": str(e)}, status=500)




 
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
