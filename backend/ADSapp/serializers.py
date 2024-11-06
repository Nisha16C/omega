from rest_framework import serializers
from django.contrib.auth.models import User
# from .models import ActiveDirectorySettings
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
 
 
# class LDAPSettingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActiveDirectorySettings
#         fields = '__all__'  # You can specify individual fields here if needed
 


 