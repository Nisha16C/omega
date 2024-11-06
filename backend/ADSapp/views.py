import os
from django.http import JsonResponse
from rest_framework import viewsets
from userAuth_app.models import User
import ldap
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from userAuth_app.permissions import IsAllowedRole
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse

from django.conf import settings

class FormViewSet(viewsets.ViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated,IsAllowedRole]
 
    def create(self, request):
 
        print('api call')
 
 
        ldap_server_uri = request.data.get('ldapServerURI')
 
        ldap_server_bind_on = request.data.get('ldapServerBIND_DN')
 
        ldap_server_bind_password = request.data.get('ldapServerBIND_PASSWORD')
 
        ldap_group_search = request.data.get('ldapGroupSearch')

        is_connected = request.data.get('True')
 
        print('ldap_server_uri', ldap_server_uri)

        print('ldapServerBIND_PASSWORD :', ldap_server_bind_password)

        try:
 
            # Read the contents of the settings.py file
 
            with open(settings.BASE_DIR / 'omega_project' / 'settings.py', 'r') as settings_file:
 
                lines = settings_file.readlines()
 
            # Write the lines back to the settings.py file, updating only the AUTH_LDAP_SERVER_URI variable
 
            with open(settings.BASE_DIR / 'omega_project' / 'settings.py', 'w') as settings_file:
 
                for line in lines:
 
                    if line.startswith('AUTH_LDAP_SERVER_URI'):
 
                        settings_file.write(f"AUTH_LDAP_SERVER_URI = '{ldap_server_uri}'\n")
 
                    elif line.startswith('AUTH_LDAP_BIND_DN'):
 
                        settings_file.write(f"AUTH_LDAP_BIND_DN = '{ldap_server_bind_on}'\n")
 
                    elif line.startswith('AUTH_LDAP_BIND_PASSWORD'):
 
                        settings_file.write(f"AUTH_LDAP_BIND_PASSWORD = '{ldap_server_bind_password}'\n")
 
                    elif line.startswith('ldapGroupSearch'):
 
                        settings_file.write(f"ldapGroupSearch = '{ldap_group_search}  '\n")

                    elif line.startswith('IS_CONNNECTED'):
 
                        settings_file.write(f"IS_CONNNECTED = '{is_connected}  '\n")

                    else:
 
                        settings_file.write(line)
 
                     # AUTH_LDAP_GROUP_SEARCH = LDAPSearch("CN=Users,DC=os3,DC=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")

 
            return JsonResponse({'message': 'LDAP settings updated successfully'}, status=200)
 
        except Exception as e:
 
            return JsonResponse({'error': str(e)}, status=500)
        
    # @api_view(['POST'])
    # @authentication_classes([TokenAuthentication])
    # @permission_classes([IsAuthenticated,IsAllowedRole])
    def reset_ldap_settings(request):
 
        try:
 
            # Update settings.py dynamically
 
            with open(os.path.join(settings.BASE_DIR, 'omega_project', 'settings.py'), 'a') as settings_file:
 
                settings_file.write("AUTH_LDAP_SERVER_URI = ''\n")
 
                settings_file.write("AUTH_LDAP_BIND_DN = ''\n")
 
                settings_file.write("AUTH_LDAP_BIND_PASSWORD = ''\n")

                settings_file.write("IS_CONNNECTED = ''\n")
 
            return JsonResponse({'message': 'LDAP settings disabled successfully'}, status=200)
 
        except Exception as e:
 
            return JsonResponse({'error': str(e)}, status=500)

 

 
from django.http import JsonResponse
 
from django_auth_ldap.backend import LDAPBackend
 
import ldap
 
def get_ad_users(request):
 
    try:
 
        # Establish LDAP connection
 
        ldap_server_uri = 'ldap://10.0.0.2:389'
 
        bind_dn = 'CN=Administrator,CN=Users,DC=os3,DC=com'
 
        bind_password = 'P@33w0rd'
 
        ldap_connection = ldap.initialize(ldap_server_uri)
 
        ldap_connection.simple_bind_s(bind_dn, bind_password)

        search_base = 'CN=Users,DC=os3,DC=com'
 
        search_filter = "(sAMAccountName=*)"  # Filter to retrieve all users
 
        ldap_users = ldap_connection.search_s(
 
            search_base,
 
            ldap.SCOPE_SUBTREE,
 
            search_filter,
 
            ['sAMAccountName']
 
        )
 
        print("ldap_users:" ,ldap_users)

        # Extract usernames
 
        user_names = [entry.get('sAMAccountName', [])[0].decode('utf-8') for dn, entry in ldap_users]

        return JsonResponse({'user_names': user_names}, safe=False)
 
    except Exception as e:
 
        return JsonResponse({'error': str(e)}, status=500)


 
 