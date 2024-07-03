from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Community, CommunityMember
from .serializers import CommunitySerializer


class CommunityCreateView(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        community = serializer.save(created_by=self.request.user)
        CommunityMember.objects.create(user=self.request.user, community=community, role='Admin')
        return Response(serializer.data)


class CommunityDeleteView(generics.DestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        community = self.get_object()
        user = request.user
        try:
            community_member = CommunityMember.objects.get(user=user, community=community, role='Admin')
            send_mail(
                f'Conferma di Cancellazione della Community "{community.name}"',
                f'Ciao {user.username},\n\nLa tua community è stata cancellata con successo.',
                'm.tucci1992@gmail.com',
                [user.email],
                fail_silently=False,
            )
        except CommunityMember.DoesNotExist:
            return Response({"error": "You do not have permission to delete this community."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().delete(request, *args, **kwargs)


class JoinCommunityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        community_id = kwargs.get('pk')
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Controlla se l'utente è già un membro della community
        if CommunityMember.objects.filter(user=user, community=community).exists():
            return Response({"error": "You are already a member of this community."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Aggiungi l'utente come membro della community
        CommunityMember.objects.create(user=user, community=community, role='Member')

        return Response({"success": "You have successfully joined the community."}, status=status.HTTP_201_CREATED)
