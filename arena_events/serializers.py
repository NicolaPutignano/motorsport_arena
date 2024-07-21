from rest_framework import serializers
from django.utils import timezone

from arena_network.constants import PROHIBITED_WORDS_EN, PROHIBITED_WORDS_IT
from arena_network.utils import contains_prohibited_words
from .models import Event, Race, RaceCar, Car, Circuit
import logging

logger = logging.getLogger(__name__)


class RaceCarSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

    class Meta:
        model = RaceCar
        fields = ['car_id', 'performance_index', 'classification', 'multiclass_group_name']


class RaceSerializer(serializers.ModelSerializer):
    cars = RaceCarSerializer(many=True)
    circuit = serializers.PrimaryKeyRelatedField(queryset=Circuit.objects.all())

    class Meta:
        model = Race
        exclude = ['event']

    def create(self, validated_data):
        cars_data = validated_data.pop('cars')
        event = self.context['event']
        race = Race.objects.create(event=event, **validated_data)
        for car_data in cars_data:
            car = Car.objects.get(id=car_data['car_id'])
            RaceCar.objects.create(race=race, car=car, **car_data)
        return race
    


class EventSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True)

    class Meta:
        model = Event
        fields = ['name', 'event_type', 'poster', 'public', 'ranked', 'document', 'races']

    def validate_name(self, value):
        if Event.objects.filter(name=value).exists():
            raise serializers.ValidationError("An event with this name already exists.")
        if contains_prohibited_words(value, PROHIBITED_WORDS_EN) or contains_prohibited_words(value,
                                                                                              PROHIBITED_WORDS_IT):
            raise serializers.ValidationError("The event name contains prohibited words.")
        return value

    def validate_document(self, value):
        if value and not value.name.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
            raise serializers.ValidationError("Only text files are allowed.")
        return value

    def validate_poster(self, value):
        if value and not value.name.lower().endswith(('.jpeg', '.jpg', '.png')):
            raise serializers.ValidationError("Only image files are allowed.")
        return value

    def validate_date(self, data):
        event_type = data.get('event_type')
        races = data.get('races')
        
        if event_type in ['Championship', 'League']:
            now = timezone.now()
            race_dates = [(race['race_start'], race) for race in races]
            invalid_dates = [race for date, race in race_dates if date <= now]
            non_sequential_dates = [race for i, (date, race) in enumerate(sorted(race_dates)) if i > 0 and date <= sorted(race_dates)[i-1][0]]

            if invalid_dates or non_sequential_dates:
                error_message = "Errore nella validazione delle gare:"
                if invalid_dates:
                    error_message += f" Le seguenti gare hanno date non valide (passate): {[race['race_start'] for race in invalid_dates]}."
                if non_sequential_dates:
                    error_message += f" Le seguenti gare non sono in ordine progressivo: {[race['race_start'] for race in non_sequential_dates]}."
                raise serializers.ValidationError(error_message)
        return data
    
    def create(self, validated_data):
        races_data = validated_data.pop('races')
        request = self.context.get('request', None)
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        event = Event.objects.create(created_by=user, status='Scheduled', **validated_data)
        logger.debug(f"Event created: {event}")
        for race_data in races_data:
            race_serializer = RaceSerializer(data=race_data, context={'event': event})
            race_serializer.is_valid(raise_exception=True)
            race_serializer.save()
            logger.debug(f"Race created: {race_serializer.data}")
        return event
