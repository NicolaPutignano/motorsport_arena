from rest_framework import generics, permissions, status
from rest_framework.response import Response

from arena_auth.authentication import CookieJWTAuthentication
from .models import Event
from .serializers import EventSerializer


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        return {'request': self.request}
