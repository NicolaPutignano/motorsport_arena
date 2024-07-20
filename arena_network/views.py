from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from arena_auth.authentication import CookieJWTAuthentication
from arena_auth.models import CustomUser
from .models import Community, CommunityMember
from .serializers import CommunitySerializer


class CommunityCreateView(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        community = serializer.save(created_by=self.request.user)
        CommunityMember.objects.create(user=self.request.user, community=community, role='Admin')
        return Response(serializer.data)


class CommunityDeleteView(generics.DestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

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
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, *args, **kwargs):
        community_name = kwargs.get('community_name')
        try:
            community = Community.objects.get(name=community_name)
        except Community.DoesNotExist:
            return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Controlla se l'utente è già un membro della community o è stato bannato in precedenza
        try:
            community_member = CommunityMember.objects.get(user=user, community=community)
            if community_member.role == 'Banned':
                return Response({"error": "You are banned from this community."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "You are already a member of this community."},
                                status=status.HTTP_400_BAD_REQUEST)
        except CommunityMember.DoesNotExist:
            pass

        # Aggiungi l'utente come membro della community
        CommunityMember.objects.create(user=user, community=community, role='Member')

        return Response({"success": "You have successfully joined the community."}, status=status.HTTP_201_CREATED)


class LeaveCommunityView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, *args, **kwargs):
        community_name = kwargs.get('community_name')
        try:
            community = Community.objects.get(name=community_name)
        except Community.DoesNotExist:
            return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            community_member = CommunityMember.objects.get(user=user, community=community)
        except CommunityMember.DoesNotExist:
            return Response({"error": "You are not a member of this community."},
                            status=status.HTTP_400_BAD_REQUEST)

        community_member.delete()
        return Response({"success": "You have successfully left the community."}, status=status.HTTP_200_OK)


class RemoveMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, *args, **kwargs):
        community_name = kwargs.get('community_name')
        username = kwargs.get('username')

        try:
            community = Community.objects.get(name=community_name)
        except Community.DoesNotExist:
            return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            member_to_remove = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Verifica se l'utente richiedente è un Admin
        try:
            admin_member = CommunityMember.objects.get(user=user, community=community, role='Admin')
        except CommunityMember.DoesNotExist:
            return Response({"error": "You do not have permission to remove members from this community."},
                            status=status.HTTP_403_FORBIDDEN)

        # Verifica se il membro da rimuovere esiste nella community
        try:
            community_member = CommunityMember.objects.get(user=member_to_remove, community=community)
        except CommunityMember.DoesNotExist:
            return Response({"error": "Member not found in this community."}, status=status.HTTP_404_NOT_FOUND)

        community_member.role = 'Banned'
        community_member.save()

        return Response({"success": "Member has been removed from the community."}, status=status.HTTP_200_OK)

