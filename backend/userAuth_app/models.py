from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models



class KeycloakUser(models.Model):
    keycloak_id = models.CharField(max_length=255, unique=True)  # Unique Keycloak ID
    username = models.CharField(max_length=150, unique=True)     # Keycloak Username
    email = models.EmailField(unique=True, null=True, blank=True)  # Email, can be blank
    nickname = models.CharField(max_length=150, null=True, blank=True)  # User's Nickname
    roles = models.JSONField(null=True, blank=True, default=list)  # JSON field to store roles as a list
    access_token = models.TextField(null=True, blank=True)  # Field to store the access token
    
    def __str__(self):
        return self.username

class Agent(models.Model):
    host_name = models.CharField(max_length=255, unique=True)  
    ip_port = models.CharField(max_length=150, unique=True)    
    keycloak_user = models.ForeignKey(
        "KeycloakUser",
        verbose_name=("Keycloak User"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )  
    agent_name = models.CharField(
        max_length=150, 
        choices=[('Linux', 'Linux'), ('Windows', 'Windows'), ('Gitlab', 'Gitlab')]
    )
    status = models.CharField(
        max_length=150, 
        choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Deleted', 'Deleted')]
    )

    def __str__(self):
        return self.host_name



class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Standard', 'Standard'),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

 
          