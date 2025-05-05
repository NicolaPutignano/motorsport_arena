import re
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model

from arena_network.constants import PROHIBITED_WORDS_EN, PROHIBITED_WORDS_IT
from arena_network.models import Community, CommunityMember
from arena_network.serializers import CommunitySerializer
from arena_network.utils import contains_prohibited_words
from .models import CustomUser, UserAttr, Nationality

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    xbox_id = serializers.CharField(write_only=True, required=True)
    accept_privacy_policy = serializers.BooleanField(write_only=True, required=True)
    accept_terms_and_conditions = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email', 'xbox_id', 'accept_privacy_policy',
                  'accept_terms_and_conditions')

    @staticmethod
    def validate_password(value):
        if value:
            if len(value) < 8:
                raise serializers.ValidationError("La password deve contenere almeno 8 caratteri.")
            if not re.search(r'[A-Z]', value):
                raise serializers.ValidationError("La password deve contenere almeno una lettera maiuscola.")
            if not re.search(r'[a-z]', value):
                raise serializers.ValidationError("La password deve contenere almeno una lettera minuscola.")
            if not re.search(r'[0-9]', value):
                raise serializers.ValidationError("La password deve contenere almeno un numero.")
            if not re.search(r'[\W_]', value):
                raise serializers.ValidationError("La password deve contenere almeno un carattere speciale.")
        return value

    def validate_password2(self, value):
        password = self.initial_data.get('password')
        if value != password:
            raise serializers.ValidationError("Le password non corrispondono")
        return value

    @staticmethod
    def validate_email(value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Formato email non valido.")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Indirizzo email già presente nel database.")
        return value

    @staticmethod
    def validate_username(value):
        if len(value) < 4 or len(value) > 16:
            raise serializers.ValidationError("L'username deve contenere tra 4 e 16 caratteri.")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("L'username può contenere solo lettere, numeri e underscore.")
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username già presente nel database.")
        if contains_prohibited_words(value, PROHIBITED_WORDS_EN) or contains_prohibited_words(value, PROHIBITED_WORDS_IT):
            raise serializers.ValidationError("L'username contiene parole proibite.")
        return value

    @staticmethod
    def validate_xbox_id(value):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9#]{2,19}$', value):
            raise serializers.ValidationError(
                "Xbox ID non valido. Deve essere lungo 3-20 caratteri,"
                " iniziare con una lettera e contenere solo lettere,"
                " numeri e il carattere '#'.")
        if '#' in value:
            parts = value.split('#')
            if len(parts) != 2:
                raise serializers.ValidationError("Xbox ID non valido. Deve contenere al massimo un carattere '#'.")
            suffix = parts[1]
            if not suffix.isdigit():
                raise serializers.ValidationError(
                    "Xbox ID non valido. Dopo il carattere '#' devono essere presenti solo numeri.")

            if len(suffix) > 4:
                raise serializers.ValidationError("Xbox ID non valido. Il suffisso non può superare 4 cifre.")
        if UserAttr.objects.filter(xbox_id=value).exists():
            raise serializers.ValidationError("ID Xbox già presente nel database.")
        return value

    @staticmethod
    def validate_accept_privacy_policy(value):
        if not value:
            raise serializers.ValidationError("Devi accettare le politiche sulla privacy.")
        return value

    @staticmethod
    def validate_accept_terms_and_conditions(value):
        if not value:
            raise serializers.ValidationError("Devi accettare i termini e condizioni")

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.pop('accept_terms_and_conditions')
        validated_data.pop('accept_privacy_policy')
        xbox_id = validated_data.pop('xbox_id')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        UserAttr.objects.create(user=user, xbox_id=xbox_id, role='Member')

        return user


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ['id', 'name', 'code']


class UserAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAttr
        fields = [
            'bio',
            'role',
            'avatar',
            'xbox_id',
            'nationality',  # Questo mostrerà l'ID della nazionalità di default
            'platform',
            'device',
            'forza_rating',
            'forza_safety_rating',
            'youtube_url',
            'twitch_url',
        ]


class CommunityMemberSerializer(serializers.ModelSerializer):
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = CommunityMember
        fields = ['id', 'community', ]


class UserProfileSerializer(serializers.ModelSerializer):
    userattr = UserAttrSerializer(read_only=True)
    communities_created = CommunitySerializer(many=True, read_only=True)

    member_of_communities = CommunityMemberSerializer(many=True, read_only=True, source='communitymember_set')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'date_joined',
            'userattr',
            'communities_created',
            'member_of_communities',
        ]
