# views.py
from rest_framework import generics
from .models import Rule
from .serializers import RuleSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
import requests
from django.http import JsonResponse
from paramiko import SSHClient, AutoAddPolicy, SSHException
from omega_project.authentication import JWTAuthentication

from rest_framework.permissions import AllowAny
 
import os
from rest_framework import viewsets
from rest_framework.response import Response
from paramiko import SSHClient, AutoAddPolicy, SSHException, RSAKey
import io
 
def save_private_key_to_file(private_key_content):
    project_folder = os.path.dirname(os.path.abspath(__file__)) 
    private_key_file_path = os.path.join(project_folder, 'private_key.pem')
    with open(private_key_file_path, 'w') as key_file:
        key_file.write(private_key_content)

    return private_key_file_path

 
class OnboardViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
 
    def create(self, request):
        try:
            server = request.data
            ip_address = server['ipAdr']
            ssh_username = server['serverUser']
            ssh_password = server['serverPass']
            print (server)
 
            project_id = "29"
            gitlab_token = "glpat-BGvtmGdaxS4u-b3yyx4o"
            base_url = 'http://gitlab-ce.os3.com/api/v4/'
            headers = {"PRIVATE-TOKEN": gitlab_token}
 
            formData = {
                "ref": "linux",
                "variables": [
                    {"key": "LINUX_HOST", "value": ip_address},
                    {"key": "LINUX_USER", "value": ssh_username},
                    {"key": "LINUX_PASSWORD", "value": ssh_password},
                ]
            }
            print(ip_address ,ssh_username,ssh_password)
            response = requests.post(base_url + f"projects/{project_id}/pipeline", headers=headers, json=formData, verify=False)
            
            if response.status_code != 201:
                return JsonResponse({'status': 'error', 'message': 'Failed to trigger pipeline'}, status=500)
 
            pipeline_id = response.json().get('id')
            if not pipeline_id:
                return JsonResponse({'status': 'error', 'message': 'No pipeline ID returned'}, status=500)
 
            # Check pipeline status periodically
            while True:
                pipeline_response = requests.get(base_url + f"projects/{project_id}/pipelines/{pipeline_id}", headers=headers, verify=False)
 
                if pipeline_response.status_code != 200:
                    return JsonResponse({'status': 'error', 'message': 'Failed to get pipeline status'}, status=500)
 
                pipeline_status = pipeline_response.json().get('status')
                if pipeline_status in ['success', 'failed']:
                    break
 
                time.sleep(5)  # Wait for 5 seconds before checking the status again
 
            if pipeline_status == 'success':
                return JsonResponse({'status': 'success', 'message': 'Pipeline succeeded'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Pipeline failed'}, status=500)
 
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

## For gitlab server bootstraping ##

 
class OnboardViewSetGitlab(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
 
    def create(self, request):
        try:
            server = request.data
            ip_address = server['ipAdr']
            ssh_username = server['serverUser']
            ssh_password = server['serverPass']
            gitlab_url = server['GitlabUrl']
            gitlab_token = server['GitlabToken']
            
            print (server)
 
            project_id = "29"
            gitlab_token = "glpat-BGvtmGdaxS4u-b3yyx4o"
            base_url = 'http://gitlab-ce.os3.com/api/v4/'
            headers = {"PRIVATE-TOKEN": gitlab_token}
 
            formData = {
                "ref": "gitlab",
                "variables": [
                    {"key": "LINUX_HOST", "value": ip_address},
                    {"key": "LINUX_USER", "value": ssh_username},
                    {"key": "LINUX_PASSWORD", "value": ssh_password},
                    {"key": "GITLAB_URL", "value":  gitlab_url},
                    {"key": "GITLAB_TOKEN", "value": gitlab_token}

                ]
            }
            print(ip_address ,ssh_username,ssh_password)
            response = requests.post(base_url + f"projects/{project_id}/pipeline", headers=headers, json=formData, verify=False)
            
            if response.status_code != 201:
                return JsonResponse({'status': 'error', 'message': 'Failed to trigger pipeline'}, status=500)
 
            pipeline_id = response.json().get('id')
            if not pipeline_id:
                return JsonResponse({'status': 'error', 'message': 'No pipeline ID returned'}, status=500)
 
            # Check pipeline status periodically
            while True:
                pipeline_response = requests.get(base_url + f"projects/{project_id}/pipelines/{pipeline_id}", headers=headers, verify=False)
 
                if pipeline_response.status_code != 200:
                    return JsonResponse({'status': 'error', 'message': 'Failed to get pipeline status'}, status=500)
 
                pipeline_status = pipeline_response.json().get('status')
                if pipeline_status in ['success', 'failed']:
                    break
 
                time.sleep(5)  # Wait for 5 seconds before checking the status again
 
            if pipeline_status == 'success':
                return JsonResponse({'status': 'success', 'message': 'Pipeline succeeded'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Pipeline failed'}, status=500)
 
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
 
## For k8s server bootstraping ##
           

class OnboardViewSetkubernetes(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
 
    def create(self, request):
        try:
            server = request.data
            kubeconfig_data = server['kubeconfig_data']
            print('data',kubeconfig_data)

            project_id = "29"
            gitlab_token = "glpat-BGvtmGdaxS4u-b3yyx4o"
            base_url = 'http://gitlab-ce.os3.com/api/v4/'
            headers = {"PRIVATE-TOKEN": gitlab_token}
 
            formData = {
                "ref": "k8s",
                "variables": [
                {"key": "CONFIG", "value": kubeconfig_data },
             ]
            }
            response = requests.post(base_url + f"projects/{project_id}/pipeline", headers=headers, json=formData, verify=False)
            
            if response.status_code != 201:
                return JsonResponse({'status': 'error', 'message': 'Failed to trigger pipeline'}, status=500)
 
            pipeline_id = response.json().get('id')
            if not pipeline_id:
                return JsonResponse({'status': 'error', 'message': 'No pipeline ID returned'}, status=500)
 
            # Check pipeline status periodically
            while True:
                pipeline_response = requests.get(base_url + f"projects/{project_id}/pipelines/{pipeline_id}", headers=headers, verify=False)
 
                if pipeline_response.status_code != 200:
                    return JsonResponse({'status': 'error', 'message': 'Failed to get pipeline status'}, status=500)
 
                pipeline_status = pipeline_response.json().get('status')
                if pipeline_status in ['success', 'failed']:
                    break
 
                time.sleep(5)  # Wait for 5 seconds before checking the status again
 
            if pipeline_status == 'success':
                return JsonResponse({'status': 'success', 'message': 'Pipeline succeeded'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Pipeline failed'}, status=500)
 
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
 
                       
 
## For  Window server bootstraping ##
 
from winrm.protocol import Protocol
from requests.exceptions import HTTPError, RequestException
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
import time
 
import winrm


class OnboardWindow(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
 
    def create(self, request):
        try:
            server = request.data
            print(server)
            ip_address = server['ipAdr']
            ssh_username = server['serverUser']
            ssh_password = server['serverPass']
 
            project_id = "29"
            gitlab_token = "glpat-BGvtmGdaxS4u-b3yyx4o"
            base_url = 'http://gitlab-ce.os3.com/api/v4/'
            headers = {"PRIVATE-TOKEN": gitlab_token}
 
            formData = {
            "ref": "windows",
            "variables": [
            {"key": "WINDOWS_HOST", "value": ip_address},
            {"key": "WINDOWS_USER", "value": ssh_username},
            {"key": "WINDOWS_PASSWORD", "value": ssh_password},
        ]
    }
            response = requests.post(base_url + f"projects/{project_id}/pipeline", headers=headers, json=formData, verify=False)
            
            if response.status_code != 201:
                return JsonResponse({'status': 'error', 'message': 'Failed to trigger pipeline'}, status=500)
 
            pipeline_id = response.json().get('id')
            if not pipeline_id:
                return JsonResponse({'status': 'error', 'message': 'No pipeline ID returned'}, status=500)
 
            # Check pipeline status periodically
            while True:
                pipeline_response = requests.get(base_url + f"projects/{project_id}/pipelines/{pipeline_id}", headers=headers, verify=False)
 
                if pipeline_response.status_code != 200:
                    return JsonResponse({'status': 'error', 'message': 'Failed to get pipeline status'}, status=500)
 
                pipeline_status = pipeline_response.json().get('status')
                if pipeline_status in ['success', 'failed']:
                    break
 
                time.sleep(5)  # Wait for 5 seconds before checking the status again
 
            if pipeline_status == 'success':
                return JsonResponse({'status': 'success', 'message': 'Pipeline succeeded'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Pipeline failed'}, status=500)
 
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
 
         
