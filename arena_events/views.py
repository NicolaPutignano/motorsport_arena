from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from arena_auth.authentication import CookieJWTAuthentication
from .models import Event, Race
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

class EventDeleteView(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def delete(self, request, *args, **kwargs):
        try:
            event = self.get.object()
        except Event.DoesNotExist:
            return Response({"detail": "Evento non trovato."}, status=status.HTTP_404_NOT_FOUND)

        # Controllo che l'utente connesso sia l'organizzatore dell'evento
        if event.created_by != request.user:
            return Response({"detail": "Non sei autorizzato a modificare questo evento."}, status=status.HTTP_403_FORBIDDEN)

        # Aggiorna lo stato dell'evento
        event.status = 'deleted'
        event.save()
        # Aggiorna lo stato delle gare associate
        Race.objects.filter(event=event).update(status='deleted')

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)