from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event, Race, Car, Circuit
from django.contrib.auth import get_user_model

User = get_user_model()

class EventSerializerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.circuit = Circuit.objects.create(name="Test Circuit", configuration="Test Configuration", length=3.5, forza_id=1)
        self.car = Car.objects.create(forza_id=1, year=2020, brand="Test Brand", model="Test Model", division="Test Division",
                                      classification="Test Classification", performance_index=100, speed=100, braking=100,
                                      handling=100, acceleration=100, power_kW=100, power_PS=100, power_hp=100, weight_kg=1000,
                                      weight_lb=2200, torque_Nm=300, torque_ftlb=221, traction="RWD", engine_position="Front",
                                      Dsp=3.5, cfg="NA", cylinders=6, ind="NA", wheel_type="Standard", doors=2, topless=False,
                                      steering_position="Left", dlc="None")

    def test_event_creation_with_valid_data(self):
        event_data = {
            "name": "Test Event",
            "event_type": "Championship",
            "public": True,
            "ranked": False,
            "poster": None,
            "document": None,
            "races": [
                {
                    "status": "Scheduled",
                    "length_type": "Laps",
                    "length": 10,
                    "initial_time_day": "Late morning",
                    "race_start": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
                    "weather": "Clear",
                    "time_progress": "Real-time",
                    "tyre_wear": 1.0,
                    "penalty": "None",
                    "box_stop": 1,
                    "circuit": self.circuit.id,
                    "cars": [
                        {
                            "car_id": self.car.id,
                            "performance_index": 100,
                            "classification": "Test Classification",
                            "multiclass_group_name": "Group 1"
                        }
                    ]
                },
                {
                    "status": "Scheduled",
                    "length_type": "Laps",
                    "length": 10,
                    "initial_time_day": "Late morning",
                    "race_start": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
                    "weather": "Clear",
                    "time_progress": "Real-time",
                    "tyre_wear": 1.0,
                    "penalty": "None",
                    "box_stop": 1,
                    "circuit": self.circuit.id,
                    "cars": [
                        {
                            "car_id": self.car.id,
                            "performance_index": 100,
                            "classification": "Test Classification",
                            "multiclass_group_name": "Group 1"
                        }
                    ]
                }
            ]
        }

        response = self.client.post('/api/events/', event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_creation_with_past_race_date(self):
        event_data = {
            "name": "Test Event",
            "event_type": "Championship",
            "public": True,
            "ranked": False,
            "poster": None,
            "document": None,
            "races": [
                {
                    "status": "Scheduled",
                    "length_type": "Laps",
                    "length": 10,
                    "initial_time_day": "Late morning",
                    "race_start": (timezone.now() - timezone.timedelta(days=1)).isoformat(),
                    "weather": "Clear",
                    "time_progress": "Real-time",
                    "tyre_wear": 1.0,
                    "penalty": "None",
                    "box_stop": 1,
                    "circuit": self.circuit.id,
                    "cars": [
                        {
                            "car_id": self.car.id,
                            "performance_index": 100,
                            "classification": "Test Classification",
                            "multiclass_group_name": "Group 1"
                        }
                    ]
                }
            ]
        }

        response = self.client.post('/api/events/', event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('All race dates must be in the future.', str(response.data))

