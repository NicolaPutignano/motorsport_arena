from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (UserRegistrationView, LogoutAndBlacklistRefreshTokenForUserView,
                    Enable2FAView, Verify2FAView, CustomTokenObtainPairView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='logout'),
    path('enable-2fa/', Enable2FAView.as_view(), name='enable_2fa'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify_2fa'),
]
