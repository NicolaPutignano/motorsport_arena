from django.db import models
from django.conf import settings

from arena_auth.models import Nationality
from arena_events.constants import EVENT_TYPES, STATUS_CHOICES, RACE_TIME_PROGRESS, RACE_PENALTY, EVENT_DOC_DIR, \
    CAR_TRACTION, CAR_ENGINE_POS


class Event(models.Model):
    name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    public = models.BooleanField(default=True)
    ranked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events_created')
    document = models.FileField(upload_to=EVENT_DOC_DIR, blank=True, null=True)

    def __str__(self):
        return self.name


class Circuit(models.Model):
    name = models.CharField(max_length=255)
    configuration = models.CharField(max_length=255)
    length = models.FloatField()
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)
    forza_id = models.IntegerField()

    def __str__(self):
        return self.name


class Car(models.Model):
    forza_id = models.IntegerField()
    year = models.IntegerField()
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    country = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)
    classification = models.CharField(max_length=255)
    performance_index = models.IntegerField()
    speed = models.FloatField()
    braking = models.FloatField()
    handling = models.FloatField()
    acceleration = models.FloatField()
    power_kW = models.IntegerField()
    power_PS = models.IntegerField()
    power_hp = models.IntegerField()
    weight_kg = models.IntegerField()
    weight_lb = models.IntegerField()
    torque_Nm = models.IntegerField()
    torque_ftlb = models.IntegerField()
    traction = models.CharField(max_length=3, choices=CAR_TRACTION)
    engine_position = models.CharField(max_length=3, choices=CAR_ENGINE_POS)
    dlc = models.BooleanField()

    def __str__(self):
        return self.model


class Race(models.Model):
    event = models.ForeignKey(Event, related_name='races', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    length = models.IntegerField()
    weather = models.CharField(max_length=100)
    race_start = models.DateTimeField()
    qualification = models.TextField()
    time_progress = models.CharField(max_length=50, choices=RACE_TIME_PROGRESS)
    timescale = models.CharField(max_length=4)
    dynamic_tyre = models.BooleanField(default=False)
    tyre_wear = models.FloatField()
    dub_ghost = models.BooleanField(default=False)
    penalty = models.CharField(max_length=20, choices=RACE_PENALTY)
    disqualified = models.BooleanField(default=False)
    box_stop = models.IntegerField()
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    cars = models.ManyToManyField(Car, through='RaceCar')

    def __str__(self):
        return f'{self.event.name} - {self.race_start}'


class RaceCar(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    performance_index = models.IntegerField()
    division = models.CharField(max_length=255)
