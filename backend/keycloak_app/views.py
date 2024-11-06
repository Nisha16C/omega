# your_app_name/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from omega_project.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

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



     

# import requests
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny

# class KeycloakTokenView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         data = request.data
#         try:
#             response = requests.post(
#                 f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
#                 data={
#                     'client_id': settings.KEYCLOAK_CLIENT_ID,
#                     'client_secret': settings.KEYCLOAK_CLIENT_SECRET_KEY,
#                     'grant_type': 'password',
#                     'username': data['username'],
#                     'password': data['password'],
#                 }
#             )
#             response.raise_for_status()
#             return Response(response.json())
#         except requests.RequestException as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # keycloak_app/views.py

# class KeycloakTokenIntrospectView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         data = request.data
#         try:
#             response = requests.post(
#                 f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token/introspect",
#                 data={
#                     'client_id': settings.KEYCLOAK_CLIENT_ID,
#                     'client_secret': settings.KEYCLOAK_CLIENT_SECRET_KEY,
#                     'token': data['token'],
#                 }
#             )
#             response.raise_for_status()
#             return Response(response.json())
#         except requests.RequestException as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# # keycloak_app/views.py

# class KeycloakLogoutView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         data = request.data
#         try:
#             response = requests.post(
#                 f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/logout",
#                 data={
#                     'client_id': settings.KEYCLOAK_CLIENT_ID,
#                     'client_secret': settings.KEYCLOAK_CLIENT_SECRET_KEY,
#                     'refresh_token': data['refresh_token'],
#                 }
#             )
#             response.raise_for_status()
#             return Response({'message': 'Successfully logged out'})
#         except requests.RequestException as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


