import pandas as pd
from django.core.management.base import BaseCommand
from arena_events.models import Circuit, Nationality


class Command(BaseCommand):
    help = 'Import circuits from an Excel file'

    def handle(self, *args, **kwargs):
        file_path = 'data/circuits_import.xlsx'
        data = pd.read_excel(file_path)

        for index, row in data.iterrows():
            nationality = Nationality.objects.get(pk=row['nationality'])
            Circuit.objects.create(
                forza_id=row['forza_id'],
                name=row['name'],
                country=nationality,
                configuration=row['configuration'],
                length=row['length'],
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported circuits'))
