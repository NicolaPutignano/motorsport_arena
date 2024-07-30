import logging

from django.db import transaction
from django.urls import reverse
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.views import APIView

from arena_auth.authentication import CookieJWTAuthentication
from .enum import EventRole
from .models import Event, EventMember
from .serializers import EventSerializer, EventDetailSerializer, EventUpdateSerializer

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

                join_url = request.build_absolute_uri(reverse('join_event', kwargs={'event_name': event.name}))

                return Response({
                    'message': f"You have successfully created the event {event.name}",
                    'join_url': join_url
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error during event creation: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        return {'request': self.request}


class JoinEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, **kwargs):
        event_name = kwargs.get('event_name')
        try:
            event = Event.objects.get(name=event_name)
        except Event.DoesNotExist:
            return Response({"error": "event not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            event_member = EventMember.objects.get(user=user, event=event)
            if event_member:
                return Response({"error": "You are already a pilot of this event."},
                                status=status.HTTP_400_BAD_REQUEST)
        except EventMember.DoesNotExist:
            pass

        EventMember.objects.create(user=user, event=event, role= EventRole.PILOT)

        return Response({"success": "You have successfully joined the event."}, status=status.HTTP_201_CREATED)


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    lookup_field = 'name'
    lookup_url_kwarg = 'event_name'

    def get(self, request, *args, **kwargs):
        event_name = self.kwargs.get(self.lookup_url_kwarg)
        try:
            event = Event.objects.get(name=event_name)
        except Event.DoesNotExist:
            return Response({"error": "event not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event)
        if event.public:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if self.request.user == event.created_by or EventMember.objects.filter(event=event,
                                                                                   user=self.request.user).exists():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You do not have permission to view this event."},
                                status=status.HTTP_401_UNAUTHORIZED)


class EventUpdateView(views.APIView):

    def patch(self, request, **kwargs):
        event_name = kwargs.get('event_name')
        event = Event.objects.get(name=event_name)
        if request.user.id != event.created_by_id:
            return Response({"error": "You do not have permission to edit this event."}, status=status.HTTP_403_FORBIDDEN)
        serializer = EventUpdateSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
