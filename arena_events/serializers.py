from django.db import transaction
from rest_framework import serializers
from django.utils import timezone

from arena_network.constants import PROHIBITED_WORDS_EN, PROHIBITED_WORDS_IT
from arena_network.utils import contains_prohibited_words
from .enum import RaceStartingTime, Status, EventTypes
from .models import Event, Race, EventCar, Car, Circuit


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = '__all__'


class EventCarSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EventCar
        fields = ['car', 'car_id', 'performance_index', 'classification', 'multiclass_group']


class RaceSerializer(serializers.ModelSerializer):
    circuit = CircuitSerializer(read_only=True)
    circuit_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Race
        fields = [
            'race_start', 'game_type', 'number_of_laps', 'race_timer', 'race_starting_time', 'custom_start_time', 'time_progress',
            'timescale', 'weather', 'dynamic_track_rubber', 'start_track_rubber_level', 'collision', 'ghost_backmarkers',
            'tire_wear', 'penalty', 'disqualified', 'box_stop', 'suggested_line', 'stm', 'tcs', 'shifting_assist',
            'steering_assist', 'throttle_assist', 'breaking_assist', 'forced_camera_view', 'circuit', 'circuit_id'
        ]

    def validate(self, data):
        if data.get('race_starting_time') == RaceStartingTime.CUSTOM and not data.get('custom_start_time'):
            raise serializers.ValidationError(
                "If race starting time is 'Custom', custom start time must be provided.")
        if data.get('time_progress') == 'Rolling' and not data.get('timescale'):
            raise serializers.ValidationError("If time progress is 'Rolling', timescale must be provided.")
        if data.get('dynamic_track_rubber') and not data.get('start_track_rubber_level'):
            raise serializers.ValidationError("If dynamic track rubber is true, start track rubber level must be provided.")
        return data

    def create(self, validated_data):
        race = Race.objects.create(**validated_data)
        return race


class EventSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True)
    cars = EventCarSerializer(many=True)

    class Meta:
        model = Event
        fields = ['name', 'event_type', 'multiclass', 'multiclass_group_name1', 'multiclass_group_name2', 'public',
                  'ranked', 'document', 'poster', 'races', 'cars']

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

        if event_type in [EventTypes.CHAMPIONSHIP, EventTypes.LEAGUE]:
            race_dates = [(race['race_start'], race) for race in races]
            non_sequential_dates = [race for i, (date, race) in enumerate(race_dates) if
                                    i > 0 and date <= race_dates[i - 1][0]]

            if non_sequential_dates:
                raise serializers.ValidationError(
                    f"Le date di inizio gara non sono consecutive"
                )

        if data.get('multiclass'):
            for car in data.get('cars', []):
                if not car.get('multiclass_group'):
                    raise serializers.ValidationError(
                        "If multiclass is true, all cars must have a multiclass group.")

        return data

    def create(self, validated_data):
        races_data = validated_data.pop('races')
        cars_data = validated_data.pop('cars')
        request = self.context.get('request', None)
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        event = Event.objects.create(created_by=user, status=Status.SCHEDULED, **validated_data)
        for race_data in races_data:
            circuit_id = race_data.pop('circuit_id')
            race = Race.objects.create(event=event, circuit_id=circuit_id, **race_data)
        for car_data in cars_data:
            car_id = car_data.pop('car_id')
            EventCar.objects.create(event=event, car_id=car_id, **car_data)
        return event


class EventDetailSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = instance.created_by.username
        return representation


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'event_type', 'public', 'ranked', 'poster', 'document', 'multiclass', 'multiclass_group_name1',
                  'multiclass_group_name2']
        read_only_fields = ['status']

    def validate(self, data):
        event = self.instance
        if event.status in [Status.Finished, Status.ARCHIVED]:
            raise serializers.ValidationError("Event cannot be modified as it is already finished or archived.")
        if event.status == Status.PROGRESS and not any(k in data for k in ['poster', 'document']):
            raise serializers.ValidationError("Only the poster and document can be updated while the event is in progress.")
        return data

    def update(self, instance, validated_data):
        if instance.status == Status.SCHEDULED:
            with transaction.atomic():
                instance = super().update(instance, validated_data)
        return instance
