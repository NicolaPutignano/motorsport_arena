from rest_framework import generics, permissions
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