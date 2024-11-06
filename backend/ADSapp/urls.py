from django.urls import path , include

# from .views import update_ldap_settings

from ADSapp.views import FormViewSet

# from .views import ActiveUserListView

from rest_framework import routers

from .views import get_ad_users 
# from .views import LDAPSettingsViewSet
 
router = routers.DefaultRouter()
 
router.register(r'update_ldap_settings', FormViewSet, basename='update_ldap_settings')

router.register(r'reset_ldap_settings', FormViewSet, basename='reset_ldap_settings')
# router.register(r'ldap-settings', LDAPSettingsViewSet, basename='ldap-settings')

urlpatterns = [
     # Define a URL pattern for accessing the LDAP users
    path('ad-users/', get_ad_users, name='ad_users_api'),
    path("", include(router.urls)),

]