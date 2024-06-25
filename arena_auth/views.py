from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer


User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)


class CustomUserRegisterView(APIView):
    def put(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registrazione avvenuta con successo."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
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