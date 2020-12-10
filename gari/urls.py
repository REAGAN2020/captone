from . import views
from django.urls import path, include
from .views import RegisterAPI, LoginAPI, UserAPI, ChangePasswordView, ServicesList, UserProfileAPI
from knox import views as knox_views
from django.conf.urls.static import static
from django.conf import settings
from . views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/', UserAPI.as_view()),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('users/<user_id>/profile/', UserProfileAPI.as_view()),
    # path('profiles/', UserProfilesAPI.as_view(), name='profiles'),
    path('services/', ServicesList.as_view(), name='services_list'),
    # path('email-verify/', VerifyEmail.as_view(),name="register"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
