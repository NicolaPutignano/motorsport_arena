from rest_framework import serializers, status
from rest_framework.response import Response

from .constants import PROHIBITED_WORDS_EN, PROHIBITED_WORDS_IT
from .models import Community
from .utils import contains_prohibited_words


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'avatar', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']

    @staticmethod
    def validate_name(value):
        if Community.objects.filter(name=value).exists():
            raise serializers.ValidationError("Una community con questo nome esiste già.")

        if contains_prohibited_words(value, PROHIBITED_WORDS_EN) or contains_prohibited_words(value, PROHIBITED_WORDS_IT):
            raise serializers.ValidationError("Il nome contiene parole proibite.")

        return value


class CommunityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['bio', 'avatar']

    def validate_bio(self, value):

        if value:
            value_lower = value.lower()
            prohibited_words = [word.lower() for word in PROHIBITED_WORDS_IT + PROHIBITED_WORDS_EN]

            for word in prohibited_words:
                if word in value_lower:
                    # Solleva un ValidationError
                    raise serializers.ValidationError("La bio contiene una parola proibita.")

        return value
