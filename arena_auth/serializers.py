import re
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser, UserAttr


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    accept_privacy_policy = serializers.BooleanField(write_only=True, required=True)
    accept_terms_and_conditions = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email', 'accept_privacy_policy', 'accept_terms_and_conditions')

    def validate_password(self, value):
        # Password should be at least 8 characters long
        if len(value) < 8:
            raise serializers.ValidationError("La password deve contenere almeno 8 caratteri.")
        # Password should contain at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La password deve contenere almeno una lettera maiuscola.")
        # Password should contain at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("La password deve contenere almeno una lettera minuscola.")
        # Password should contain at least one number
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("La password deve contenere almeno un numero.")
        # Password should contain at least one special character
        if not re.search(r'[\W_]', value):
            raise serializers.ValidationError("La password deve contenere almeno un carattere speciale.")
        return value

    def validate_email(self, value):
        # Check if email format is valid
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Formato email non valido.")
        # Check if email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Indirizzo email già presente nel database.")
        return value

    def validate_username(self, value):
        # Check if username is unique
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username già presente nel database.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Le password non corrispondono."})
        if not attrs['email']:
            raise serializers.ValidationError({"email": "Devi inserire un email"})
        if not attrs['accept_privacy_policy']:
            raise serializers.ValidationError({"accept_privacy_policy": "Devi accettare le politiche sulla privacy."})
        if not attrs['accept_terms_and_conditions']:
            raise serializers.ValidationError({"accept_terms_and_conditions": "Devi accettare i termini e condizioni"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.pop('accept_terms_and_conditions')
        validated_data.pop('accept_privacy_policy')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
