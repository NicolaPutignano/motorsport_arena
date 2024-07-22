from rest_framework import serializers
from django.utils import timezone

from arena_network.constants import PROHIBITED_WORDS_EN, PROHIBITED_WORDS_IT
from arena_network.utils import contains_prohibited_words
from .models import Event, Race, RaceCar, Car, Circuit


class RaceCarSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = RaceCar
        fields = ['car', 'performance_index', 'classification', 'multiclass_group_name']


class RaceSerializer(serializers.ModelSerializer):
    cars = RaceCarSerializer(many=True)
    circuit = serializers.PrimaryKeyRelatedField(queryset=Circuit.objects.all())

    class Meta:
        model = Race
        fields = [
            'length_type', 'length', 'initial_time_day', 'start_time_game', 'weather', 'race_start',
            'qualification', 'time_progress', 'timescale', 'dynamic_tyre', 'tyre_on_track', 'tyre_wear',
            'collision', 'dub_ghost', 'penalty', 'disqualified', 'box_stop', 'restrictions',
            'multiclass', 'circuit', 'cars'
        ]

    def validate(self, data):
        if data.get('multiclass'):
            for car in data.get('cars', []):
                if not car.get('multiclass_group_name'):
                    raise serializers.ValidationError(
                        "If multiclass is true, all cars must have a multiclass_group_name.")
        if data.get('initial_time_day') == 'Personalized' and not data.get('start_time_game'):
            raise serializers.ValidationError(
                "If initial_time_day is 'Personalized', start_time_game must be provided.")
        if data.get('time_progress') == 'Continuous' and not data.get('timescale'):
            raise serializers.ValidationError("If time_progress is 'Continuous', timescale must be provided.")
        if data.get('dynamic_tyre') and not data.get('tyre_on_track'):
            raise serializers.ValidationError("If dynamic_tyre is true, tyre_on_track must be provided.")
        return data

    def create(self, validated_data):
        cars_data = validated_data.pop('cars')
        race = Race.objects.create(**validated_data)
        for car_data in cars_data:
            RaceCar.objects.create(race=race, **car_data)
        return race


class EventSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True)

    class Meta:
        model = Event
        fields = ['name', 'event_type', 'public', 'ranked', 'document', 'poster', 'races']

    def validate_name(self, value):
        if Event.objects.filter(name=value).exists():
            raise serializers.ValidationError("An event with this name already exists.")
        if contains_prohibited_words(value, PROHIBITED_WORDS_EN) or contains_prohibited_words(value, PROHIBITED_WORDS_IT):
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

    def validate(self, data):
        event_type = data.get('event_type')
        races = data.get('races')
        now = timezone.now()

        if event_type == 'SingleRace' and len(races) != 1:
            raise serializers.ValidationError("A SingleRace event must contain exactly one race.")
        if event_type in ['Championship', 'League'] and len(races) <= 2:
            raise serializers.ValidationError("A Championship or League event must contain more than two races.")

        invalid_dates = [race for race in races if race['race_start'] <= now]

        if invalid_dates:
            raise serializers.ValidationError(
                f"Hai indicato una data per l'inizio di una gara, antecedenti alla data odierna"
            )

        if event_type in ['Championship', 'League']:
            race_dates = [(race['race_start'], race) for race in races]
            non_sequential_dates = [race for i, (date, race) in enumerate(race_dates) if
                                    i > 0 and date <= race_dates[i - 1][0]]

            if non_sequential_dates:
                raise serializers.ValidationError(
                    f"Le date di inizio gara non sono consecutive"
                )

        return data

    def create(self, validated_data):
        races_data = validated_data.pop('races')
        request = self.context.get('request', None)
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        event = Event.objects.create(created_by=user, status='Scheduled', **validated_data)
        for race_data in races_data:
            cars_data = race_data.pop('cars')
            race = Race.objects.create(event=event, **race_data)
            for car_data in cars_data:
                RaceCar.objects.create(race=race, **car_data)
        return event
