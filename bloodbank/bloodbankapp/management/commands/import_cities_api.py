# management/commands/import_cities_api.py
import requests
from django.core.management.base import BaseCommand
from bloodbankapp.models import City


class Command(BaseCommand):
    help = 'Import cities from an API'

    def handle(self, *args, **kwargs):
        # Example using a geocoding API
        api_url = "https://api.example.com/cities"
        response = requests.get(api_url)

        if response.status_code == 200:
            cities_data = response.json()
            for city in cities_data:
                City.objects.create(
                    name=city['name'],
                    state=city['state'],
                    latitude=city['latitude'],
                    longitude=city['longitude']
                )
            self.stdout.write(self.style.SUCCESS(f'Imported {len(cities_data)} cities'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch city data'))