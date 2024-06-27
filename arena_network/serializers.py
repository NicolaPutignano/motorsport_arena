from rest_framework import serializers
from .models import Community


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'avatar', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']
