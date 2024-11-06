"""
Django settings for multi_role_auth project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv

#LDAP Configurations
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from environs import Env


# Set up environs
env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-k-4q9^e*k!gn+(t*d_ayl-p_lqw0)f@d($=+qh-0$1rv1s*8^4'
SECRET_KEY = env.str("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

# DEBUG = True

ALLOWED_HOSTS = ['172.16.1.190','localhost', '172.16.1.158', '172.16.1.190']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'rest_framework',
    'rest_framework.authtoken',
    'userAuth_app',
    'rule__api',
    'ADSapp',
    'drf_yasg',
    'keycloak_app',



]

AUTH_USER_MODEL = 'userAuth_app.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'keycloak_app.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'keycloak_app.middleware.KeycloakMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = 'omega_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'omega_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = [
    # 'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    # 'keycloak_app.backends.KeycloakAuthorizationCodeBackend'
]

KEYCLOAK_CONFIG = {
    'REALM': 'master',
    'SERVER_URL': 'http://172.16.1.158:8080',
    'CLIENT_ID': 'account',  # Replace with your actual client ID
}

# KEYCLOAK_SERVER_URL = "http://172.16.1.158:8080"
# KEYCLOAK_REALM = "aastha-relm"
# KEYCLOAK_CLIENT_ID = "aastha-client"
# KEYCLOAK_CLIENT_SECRET_KEY = "QkJ2VxJQr5Xj0LAttatRtGl2Q3lPdCJ7"
# KEYCLOAK_AUTO_OPENID = True




IS_CONNNECTED = 'True  '
 
ldapGroupSearch = 'CN=Users,DC=os3,DC=com   '
 
 
AUTH_LDAP_SERVER_URI = 'ldap://10.0.0.2:389'
AUTH_LDAP_BIND_DN = 'CN=Administrator,CN=Users,DC=os3,DC=com'
AUTH_LDAP_BIND_PASSWORD = 'P@33w0rd'
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    ldapGroupSearch,  # Use ldapGroupSearchBase here
    ldap.SCOPE_SUBTREE,
    "(sAMAccountName=%(user)s)"
)
 
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("CN=Users,DC=example,DC=com", ldap.SCOPE_SUBTREE, "(objectClass=group)")
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
 
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "giveName",
    "last_name": "sn",
    "email": "mail"
}


 


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:9980",
    "http://172.16.1.190:3000" ,
    "http://172.16.1.190:9980"   

]