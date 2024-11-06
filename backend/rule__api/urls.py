# urls.py
from django.urls import path
from .views import  *
from django.contrib import admin
from django.urls import path,include

from rest_framework import routers
# from . import views


router = routers.DefaultRouter()
# router.register(r'users', UserAuthViewSet, basename="register")

router.register(r'onboard', OnboardViewSet, basename='onboard')
router.register(r'OnboardGitlab', OnboardViewSetGitlab, basename='OnboardViewSetGitlab')

router.register(r'onboardWindow', OnboardWindow, basename='onboardWindow')
router.register(r'onboardkubernetes',  OnboardViewSetkubernetes , basename=' OnboardViewSetkubernetes ')


urlpatterns = [
    # ... your other patterns
    path("", include(router.urls))
]
