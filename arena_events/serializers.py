from rest_framework import serializers

from arena_network.constants import PROHIBITED_WORDS_EN, PROHIBITED_WORDS_IT
from arena_network.utils import contains_prohibited_words
from .models import Event, Race, RaceCar, Car


class RaceCarSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

    class Meta:
        model = RaceCar
        fields = ['car_id', 'performance_index', 'division']

    def create(self, validated_data):
        race = validated_data.get('race')
        car_id = validated_data.get('car_id')
        performance_index = validated_data.get('performance_index')
        division = validated_data.get('division')

        car = Car.objects.get(id=car_id)
        return RaceCar.objects.create(race=race, car=car, performance_index=performance_index, division=division)


class RaceSerializer(serializers.ModelSerializer):
    cars = RaceCarSerializer(many=True)

    class Meta:
        model = Race
        fields = '__all__'

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
        fields = '__all__'

    def validate_name(self, value):
        if Event.objects.filter(name=value).exists():
            raise serializers.ValidationError("An event with this name already exists.")
        if contains_prohibited_words(value, PROHIBITED_WORDS_EN) or contains_prohibited_words(value,
                                                                                              PROHIBITED_WORDS_IT):
            raise serializers.ValidationError("The event name contains prohibited words.")
        return value

    def create(self, validated_data):
        races_data = validated_data.pop('races')
        event = Event.objects.create(**validated_data)
        for race_data in races_data:
            cars_data = race_data.pop('cars')
            race = Race.objects.create(event=event, **race_data)
            for car_data in cars_data:
                car_id = car_data.pop('car_id')
                car = Car.objects.get(id=car_id)
                RaceCar.objects.create(race=race, car=car, **car_data)
        return event
