from django.db import models
from django.conf import settings
from arena_network.constants import EVENT_DOC_DIR


class Community(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='communities_created')

    def __str__(self):
        return self.name


class CommunityMember(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Member', 'Member'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'community')

    def __str__(self):
        return f'{self.user.username} in {self.community.name} as {self.role}'
    
class Event(models.Model):
    name_event = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to=EVENT_DOC_DIR, null=True, blank=True)

    def __str__(self):
        return self.name_event

class Race(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races')
    status = models.CharField(max_length=100)
    length = models.FloatField()
    weather = models.CharField(max_length=100)
    race_start = models.DateTimeField()
    qualification = models.CharField(max_length=255)
    time_progress = models.CharField(max_length=10)
    dynamic_tyre = models.BooleanField()
    tyre_wear = models.FloatField()
    dub_ghost = models.BooleanField()
    penalty = models.CharField(max_length=255)
    disqualified = models.BooleanField()
    box_stop = models.IntegerField()

    def __str__(self):
        return f"{self.event.name_event} - {self.status}"

class Car(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='cars')
    model = models.CharField(max_length=100)
    driver = models.CharField(max_length=100)
    performance_rating = models.FloatField()

    def __str__(self):
        return f"{self.model} - {self.driver}"

class Circuit(models.Model):
    race = models.OneToOneField(Race, on_delete=models.CASCADE, related_name='circuit')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    length = models.FloatField()

    def __str__(self):
        return self.name
    
class RaceCircuit(models.Model):
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    order = models.IntegerField()
    division = models.CharField(max_length=255)
    
    def __str__(self):
        return f"RaceCircuit {self.pk}: Event {self.id_event.name_event}, Circuit {self.id_circuit.name}, Order {self.order}, Division {self.division}"
    
class RaceCar(models.Model):
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    performance_index = models.IntegerField()
    division = models.CharField(max_length=255)

    def __str__(self):
        return f"RaceCar {self.pk}: Event {self.id_event.name_event}, Car {self.id_car.model}, Indice Prestazione {self.performance_index}, Division {self.division}"
    
class EventUser(models.Model):
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField()
    point = models.IntegerField()

    def __str__(self):
        return f"EventUser {self.pk}: Event {self.id_event.name_event}, User {self.id_user.username}, Posizione {self.position}, Punteggio {self.point}"
