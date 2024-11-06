# multi_role_auth/urls.py

from django.urls import path, include, re_path
from userAuth_app.views import get_ADgroup_users, IsConnectedAPIView,schema_view, UserRegistrationView, assign_or_change_role, UserRoleAPIView, LDAPLoginView, UserLoginView,assign_roles_to_adgroup_members,get_adgroup_role, UserLogoutView, user_details, UserListView, save_ad_users, list_ad_groups_with_members
from .views import schema_view


urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('ldap-login/', LDAPLoginView.as_view(), name='lda-user-login'),
    path('get-user-info/', user_details, name='user_details'),  
    path('users/', UserListView.as_view(), name='user-list'),  # Add this line
    path('save-ad-users/', save_ad_users, name='save_ad_users'),
    path('list-gmember/', list_ad_groups_with_members, name='list_ad_groups_with_members'),
    path('fetch-group-role/<str:group_name>/', get_adgroup_role, name='get_adgroup_role'),
    path('assign-role-group/', assign_roles_to_adgroup_members, name='assign_roles_to_adgroup_members'),
    path('users/<str:username>/assign-role/', assign_or_change_role, name='assign_or_change_role'),
    path('users/<str:username>/user-role/', UserRoleAPIView.as_view(), name='user_role_api'),
    path('is-connected/', IsConnectedAPIView.as_view(), name='user-list'),  # Add this line


    path('save-ad-groups/', get_ADgroup_users, name='get_ADgroup_users'),    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


    