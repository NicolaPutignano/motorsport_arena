from rest_framework import serializers
from .constants import PROHIBITED_WORDS_EN, PROHIBITED_WORDS_IT
from .models import Community
from .utils import contains_prohibited_words


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'avatar', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']

    def validate_name(self, value):
        if Community.objects.filter(name=value).exists():
            raise serializers.ValidationError("Una community con questo nome esiste già.")

        if contains_prohibited_words(value, PROHIBITED_WORDS_EN) or contains_prohibited_words(value, PROHIBITED_WORDS_IT):
            raise serializers.ValidationError("Il nome contiene parole proibite.")

        return value
