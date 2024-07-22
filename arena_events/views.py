import json
import logging

from django.core import serializers
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from arena_auth.authentication import CookieJWTAuthentication
from .models import Event
from .serializers import EventSerializer

logger = logging.getLogger(__name__)


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        try:
            with transaction.atomic():
                event_serializer = self.get_serializer(data=data)
                event_serializer.is_valid(raise_exception=True)
                event = event_serializer.save()

                event_json = serializers.serialize('json', [event])
                event_data = json.loads(event_json)[0]

                return Response(event_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error during event creation: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        return {'request': self.request}
