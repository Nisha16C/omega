from django.contrib import admin
from .models import User ,KeycloakUser, Agent

admin.site.register(User)
admin.site.register(KeycloakUser) 
admin.site.register(Agent) 



