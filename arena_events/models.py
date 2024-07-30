from django.db import models
from django.conf import settings

from arena_auth.models import Nationality
from arena_events.constants import EVENT_DOC_DIR, CAR_TRACTION, CAR_ENGINE_POS, CAR_WHEEL_TYPE, CAR_STEER_POS, CFG, \
    IND, EVENT_ROLE_CHOICES
from arena_events.enum import EventTypes, Status, RaceGameType, RaceStartingTime, RaceTimeProgress, RaceWeather, \
    RacePenalty, RaceShifting, RaceSteering, RaceCameraView, RaceBreakingAssist


class Event(models.Model):
    name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20, choices=EventTypes.choices)
    multiclass = models.BooleanField(default=False)
    multiclass_group_name1 = models.CharField(max_length=255, blank=True, null=True)
    multiclass_group_name2 = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    public = models.BooleanField(default=True)
    ranked = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='events/poster/', blank=True, null=True)
    document = models.FileField(upload_to=EVENT_DOC_DIR, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events_created')

    def __str__(self):
        return self.name


class Circuit(models.Model):
    name = models.CharField(max_length=255)
    configuration = models.CharField(max_length=255)
    length = models.FloatField()
    country = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)
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
    traction = models.CharField(max_length=10, choices=CAR_TRACTION)
    engine_position = models.CharField(max_length=10, choices=CAR_ENGINE_POS)
    Dsp = models.FloatField()
    cfg = models.CharField(max_length=10, choices=CFG)
    cylinders = models.IntegerField()
    ind = models.CharField(max_length=10, choices=IND)
    wheel_type = models.CharField(max_length=10, choices=CAR_WHEEL_TYPE)
    doors = models.IntegerField()
    topless = models.BooleanField()
    steering_position = models.CharField(max_length=10, choices=CAR_STEER_POS)
    dlc = models.CharField(max_length=255)

    def __str__(self):
        return self.model


class Race(models.Model):
    event = models.ForeignKey(Event, related_name='races', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    race_start = models.DateTimeField()
    qualification = models.TextField(blank=True, null=True)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    cars = models.ManyToManyField(Car, through='RaceCar')
    game_type = models.CharField(max_length=20, choices=RaceGameType.choices, default=RaceGameType.CIRCUIT_RACE)
    number_of_laps = models.IntegerField()
    race_timer = models.IntegerField()
    race_starting_time = models.CharField(max_length=100, choices=RaceStartingTime.choices,
                                          default=RaceStartingTime.LATE_MORNING)
    custom_start_time = models.CharField(max_length=5, blank=True, null=True)
    time_progress = models.CharField(max_length=50, choices=RaceTimeProgress.choices)
    timescale = models.CharField(max_length=4, blank=True, null=True)
    weather = models.CharField(max_length=100, choices=RaceWeather.choices)
    dynamic_track_rubber = models.BooleanField(default=False)
    start_track_rubber_level = models.IntegerField(default=50, blank=True, null=True)
    collision = models.BooleanField(default=False)
    ghost_backmarkers = models.BooleanField(default=False)
    tire_wear = models.FloatField()
    penalty = models.CharField(max_length=20, choices=RacePenalty.choices)
    disqualified = models.BooleanField(default=False)
    box_stop = models.IntegerField()
    suggested_line = models.BooleanField(default=False)
    stm = models.BooleanField(default=False)
    tcs = models.BooleanField(default=False)
    shifting_assist = models.CharField(max_length=20, choices=RaceShifting.choices, default=RaceShifting.AUTOMATIC)
    steering_assist = models.CharField(max_length=20, choices=RaceSteering.choices, default=RaceSteering.FULLY)
    throttle_assist = models.BooleanField(default=False)
    breaking_assist = models.CharField(max_length=20, choices=RaceBreakingAssist.choices,
                                       default=RaceBreakingAssist.ASSISTED)
    forced_camera_view = models.CharField(max_length=20, choices=RaceCameraView.choices, default=RaceCameraView.NONE)

    def __str__(self):
        return f'{self.event.name} - {self.race_start}'


class RaceCar(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    performance_index = models.IntegerField()
    classification = models.CharField(max_length=255)
    multiclass_group = models.IntegerField(blank=True, null=True)


class EventMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=10, choices=EVENT_ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.username} in {self.event.name} as {self.role}'
