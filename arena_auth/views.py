from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings

from .authentication import CookieJWTAuthentication
from .serializers import CustomUserSerializer, LogoutSerializer


User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)


class CustomTokenObtainPairView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                response = Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=str(refresh),
                    httponly=True,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'],
                    value=str(refresh.access_token),
                    httponly=True,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                return response
            else:
                return Response({"detail": "User account is disabled."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh_token']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Enable2FAView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
        if created:
            return Response({'status': '2FA enabled', 'otp_secret': device.config_url})
        return Response({'status': '2FA already enabled'}, status=status.HTTP_400_BAD_REQUEST)


class Verify2FAView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        token = request.data.get('token')
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if device and device.verify_token(token):
            return Response({'status': '2FA verified'})
        return Response({'status': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        email = user.email
        username = user.username
        user.delete()

        # Invia un'email di conferma
        send_mail(
            'Conferma di Cancellazione dell\'Account',
            f'Ciao {username},\n\nIl tuo account è stato cancellato con successo.',
            'm.tucci1992@gmail.com',
            [email],
            fail_silently=False,
        )

        return Response({"detail": "Account cancellato con successo. Una email di conferma è stata inviata."},
                        status=status.HTTP_200_OK)
