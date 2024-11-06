# userAuth_app/views.py

from userAuth_app.models import User
from userAuth_app.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.conf import settings

from .models import LDAPGroup, LDAPGroupMember,ADGroupRoleAssignment


from django_auth_ldap.backend import LDAPBackend
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics
from .serializers import UserListSerializer
from rest_framework import permissions


import ldap




from rest_framework.permissions import IsAuthenticated
from userAuth_app.permissions import IsAllowedRole
from rest_framework.authentication import TokenAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from .views import schema_view


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema

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

            



class LDAPLoginView(ObtainAuthToken):
    # authentication_classes = [TokenAuthentication]
    @swagger_auto_schema(
        operation_description="AD user login",
        request_body=UserSerializer,
        manual_parameters=[token_param_config],
        responses={201: 'Created', 400: 'Bad Request'}
    )

    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate using LDAPBackend
        ldap_backend = LDAPBackend()
        user = ldap_backend.authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # # Check if the user already has a project assigned
            # existing_project = Project.objects.filter(user=user).first()

            # if existing_project:
            #     # User already has a project assigned
            #     project_name = existing_project.project_name
            # else:
            #     # Generate a random project name and assign it to the user
            #     project_name = self.generate_random_project_name()

            #     # Create a new project and associate it with the user
            #     Project.objects.create(user=user, project_name=project_name)
            
            # Generate or retrieve token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Return response with token, username, role, and project name
            return Response({
                'token': token.key,
                'username': user.username,
                'role': user.role,
                # 'project_name': project_name
            })

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserListView(generics.ListAPIView):

   
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated] 
    
     

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        # add other details as needed
    })


# User role view
class UserRoleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserRoleSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def save_ad_users(request):
    try:
        # Establish LDAP connection
        ldap_server_uri = 'ldap://10.0.0.2:389'
        bind_dn = 'CN=Administrator,CN=Users,DC=os3,DC=com'
        bind_password = 'P@33w0rd'
        
        ldap_connection = ldap.initialize(ldap_server_uri)
        ldap_connection.simple_bind_s(bind_dn, bind_password)
        
        # Search base and filter
        search_base = 'CN=Users,DC=os3,DC=com'
        search_filter = "(objectClass=user)"  # Filter to retrieve all users
        
        # Specify attributes to retrieve
        attributes = ['sAMAccountName']  # Only retrieving sAMAccountName
        
        # Search for users
        ldap_users = ldap_connection.search_s(
            search_base,
            ldap.SCOPE_SUBTREE,
            search_filter,
            attributes
        )
        
        # Extract sAMAccountName and save to the database
        user_data = []

        for dn, entry in ldap_users:
            if 'sAMAccountName' in entry:
                sam_account_name = entry['sAMAccountName'][0].decode('utf-8')
                # Save the sAMAccountName to the User model if not already present
                if not User.objects.filter(username=sam_account_name).exists():
                    User.objects.create(username=sam_account_name)
                user_data.append({'sAMAccountName': sam_account_name})
        
        return JsonResponse({'users': user_data}, safe=False)
    
    except ldap.LDAPError as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_ADgroup_users(request):
    try:
        # Establish LDAP connection
        ldap_server_uri = 'ldap://10.0.0.2:389'
        bind_dn = 'CN=Administrator,CN=Users,DC=os3,DC=com'
        bind_password = 'P@33w0rd'
        ldap_connection = ldap.initialize(ldap_server_uri)
        ldap_connection.simple_bind_s(bind_dn, bind_password)
 
        # Search for all groups
        search_base_groups = 'CN=Users,DC=os3,DC=com'
        search_filter_groups = "(objectClass=group)"
        ldap_groups = ldap_connection.search_s(
            search_base_groups,
            ldap.SCOPE_SUBTREE,
            search_filter_groups,
            ['sAMAccountName', 'member']
        )
 
        # Iterate over LDAP groups
        for dn, entry in ldap_groups:
            group_name = entry.get('sAMAccountName', [])[0].decode('utf-8')
            print("group_name", group_name)
 
            # Check if the group already exists in the database
            ldap_group, created = LDAPGroup.objects.get_or_create(name=group_name)
 
            # Retrieve and save member sAMAccountName
            members = entry.get('member', [])
            for member in members:
                member_dn = member.decode('utf-8')
                # Fetch the member's sAMAccountName
                member_info = ldap_connection.search_s(
                    member_dn,
                    ldap.SCOPE_BASE,
                    '(objectClass=*)',
                    ['sAMAccountName']
                )
                if member_info:
                    member_name = member_info[0][1].get('sAMAccountName', [])[0].decode('utf-8')
                    print("member_name", member_name)
                    # Save group member if not already exists
                    LDAPGroupMember.objects.get_or_create(group=ldap_group, username=member_name)
 
        return JsonResponse({'message': 'LDAP groups and members saved successfully'})
 
    except ldap.LDAPError as e:
        return JsonResponse({'error': str(e)}, status=500)
 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_ad_groups_with_members(request):

    try:
        # Establish LDAP connection
        ldap_server_uri = 'ldap://10.0.0.2:389'
        bind_dn = 'CN=Administrator,CN=Users,DC=os3,DC=com'
        bind_password = 'P@33w0rd'
        ldap_connection = ldap.initialize(ldap_server_uri)
        ldap_connection.simple_bind_s(bind_dn, bind_password)

        # Search for all groups
        search_base_groups = 'CN=Users,DC=os3,DC=com'
        search_filter_groups = "(objectClass=group)"
        ldap_groups = ldap_connection.search_s(
            search_base_groups,
            ldap.SCOPE_SUBTREE,
            search_filter_groups,
            ['sAMAccountName', 'member']
        )

        group_info = []

        for dn, entry in ldap_groups:
            group_name = entry.get('sAMAccountName', [])[0].decode('utf-8')
            members = entry.get('member', [])
            member_names = []

            for member in members:
                member_dn = member.decode('utf-8')
                # Fetch the member's sAMAccountName
                member_info = ldap_connection.search_s(
                    member_dn,
                    ldap.SCOPE_BASE,
                    '(objectClass=*)',
                    ['sAMAccountName']
                )
                if member_info:
                    member_name = member_info[0][1].get('sAMAccountName', [])[0].decode('utf-8')
                    member_names.append(member_name)

            group_info.append({
                'group_name': group_name,
                'members': member_names
            })

        return JsonResponse({'groups': group_info}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def assign_or_change_role(request, username):
    try:
        user = User.objects.get(username=username)
        role = request.data.get('role')

        if role not in dict(User.ROLE_CHOICES).keys():
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()
        # Log the role assignment event
        log_entry = f"user={user.username} msg=Role changed to: {role}"
        # role_assignment_logger.info(log_entry)

        return Response({'message': f'Role for {username} changed to {role}'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

#role assign in view page pe
def assign_roles_to_adgroup_members(request):
    if request.method == 'POST':
        group_name = request.data.get('group_name')
        role_name = request.data.get('role_name')
        sAMAccountNames = request.data.get('sAMAccountNames')

        if not group_name or not role_name or not sAMAccountNames:
            return Response({'success': False, 'message': 'group_name, role_name, and sAMAccountNames are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the group object
            group = LDAPGroup.objects.get(name=group_name)

            # Find the group members
            group_members = LDAPGroupMember.objects.filter(group=group)

            # Assign the new role to each user
            for member in group_members:
                user, _ = User.objects.get_or_create(username=member.username)
                user.role = role_name  # Assuming you can directly set the role field
                user.save()

            # Create or update ADGroupRoleAssignment
            ad_group_assignment, _ = ADGroupRoleAssignment.objects.update_or_create(
                group_name=group_name,
                defaults={'role_name': role_name}
            )

            # log_entry = f"group={group_name}, role={role_name}, msg=role assign to group, sAMAccountNames={sAMAccountNames}"
            # Grouprole_assignment_logger.info(log_entry)

            return Response({'success': True, 'message': f'Roles assigned to members of {group_name}'})
        except LDAPGroup.DoesNotExist:
            log_entry = f"msg=Failed role assignment group_name={group_name} reason=Group does not exist"
            Grouprole_assignment_logger.info(log_entry)
            return Response({'success': False, 'message': f'Group {group_name} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log_entry = f"msg=Failed role assignment group_name={group_name} reason={str(e)}"
            Grouprole_assignment_logger.error(log_entry)
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'success': False, 'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class UserRoleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserRoleSerializer(user)
            return Response({'role': serializer.data['role']}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_adgroup_role(request, group_name):
    print("11111calling function")
    
    try:
        print ("group_name", group_name)

        print("calling function")
        # print("decoded_group_name",urllib.parse.unquote(group_name))
        print ("group_name", group_name)


        # Decode the group name
        # decoded_group_name = urllib.parse.unquote(group_name)

        
        # Fetch the AD group role assignment
        ad_group_role_assignment = ADGroupRoleAssignment.objects.get(group_name=group_name)
        
        print(ad_group_role_assignment)
        role_name = ad_group_role_assignment.role_name
        print(role_name)
        return Response({'success': True, 'group_name': group_name, 'role_name': role_name})
    except ADGroupRoleAssignment.DoesNotExist:
        return Response({'success': False, 'message': f'No role assigned to group {decoded_group_name}'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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


class IsConnectedAPIView(APIView):
    # authentication_classes = [TokenAuthentication]   
    # permission_classes = [IsAuthenticated,IsAllowedRole]
    def get(self, request):

        is_connected = settings.IS_CONNNECTED.strip()  # Corrected attribute name and stripping whitespace
        print("is_connected", is_connected)
        return Response({'is_connected': is_connected})


        
    