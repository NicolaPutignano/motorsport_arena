import pandas as pd
from django.core.management.base import BaseCommand
from arena_events.models import Car, Nationality


class Command(BaseCommand):
    help = 'Import cars from an Excel file'

    def handle(self, *args, **kwargs):
        file_path = 'data/modelexport.xlsx'
        data = pd.read_excel(file_path)

        for index, row in data.iterrows():
            nationality, created = Nationality.objects.get_or_create(name=row['country'])
            Car.objects.create(
                forza_id=row['forza_id'],
                year=row['year'],
                brand=row['brand'],
                model=row['model'],
                division=row['division'],
                country=nationality,
                classification=row['classification'],
                performance_index=row['performance_index'],
                speed=row['speed'],
                braking=row['braking'],
                handling=row['handling'],
                acceleration=row['acceleration'],
                power_kW=row['power_kW'],
                power_PS=row['power_PS'],
                power_hp=row['power_hp'],
                weight_kg=row['weight_kg'],
                weight_lb=row['weight_lb'],
                torque_Nm=row['torque_Nm'],
                torque_ftlb=row['torque_ftlb'],
                traction=row['traction'],
                engine_position=row['engine_position'],
                Dsp=row['Dsp'],
                cfg=row['cfg'],
                cylinders=row['cylinders'],
                ind=row['ind'],
                wheel_type=row['wheel_type'],
                doors=row['doors'],
                topless=row['topless'],
                steering_position=row['steering_position'],
                dlc=row['dlc'],
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported cars'))
