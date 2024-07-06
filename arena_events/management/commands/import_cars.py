import pandas as pd
from django.core.management.base import BaseCommand
from arena_events.models import Car, Nationality


class Command(BaseCommand):
    help = 'Import cars from an Excel file'

    def handle(self, *args, **kwargs):
        file_path = 'data/cars_model_import.xlsx'
        data = pd.read_excel(file_path)

        for index, row in data.iterrows():
            nationality = Nationality.objects.get(pk=row['country'])
            Car.objects.create(
                forza_id=row['forza_id'],
                year=row['year'],
                brand=row['brand'],
                model=row['model'],
                division=row['division'],
                country=nationality,
                classification=row['classification'],
                performance_index=row['performance_index'],
                speed=row['S'],
                braking=row['B'],
                handling=row['H'],
                acceleration=row['A'],
                power_kW=row['Pwr kW'],
                power_PS=row['Pwr PS'],
                power_hp=row['Pwr hp'],
                weight_kg=row['Mass kg'],
                weight_lb=row['Mass lb'],
                torque_Nm=row['Trq N.m'],
                torque_ftlb=row['Trq ft-lb'],
                traction=row['Drvtr.'],
                engine_position=row['Eng.pos.'],
                Dsp=row['Dsp.'],
                cfg=row['Cfg.'],
                cylinders=row['Cyl.'],
                ind=row['Ind.'],
                wheel_type=row['Type'],
                doors=row['Doors'],
                topless=row['Topless'],
                steering_position=row['Steer.pos.'],
                dlc=row['dlc'],
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported cars'))
