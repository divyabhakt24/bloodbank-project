from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from time import sleep
from bloodbankapp.models import BloodBank


class Command(BaseCommand):
    help = 'Geocode existing BloodBank entries without coordinates'

    def handle(self, *args, **options):
        geolocator = Nominatim(user_agent="bloodbank_app")
        # Only process records where address exists but coordinates don't
        banks = BloodBank.objects.filter(address__isnull=False).filter(
            latitude__isnull=True,
            longitude__isnull=True
        )

        self.stdout.write(f"Found {banks.count()} banks needing geocoding...")

        for bank in banks:
            try:
                location = geolocator.geocode(bank.address)
                sleep(1)  # Respect Nominatim's rate limit

                if location:
                    bank.latitude = location.latitude
                    bank.longitude = location.longitude
                    bank.save()
                    self.stdout.write(f"Geocoded: {bank.name} ({bank.latitude}, {bank.longitude})")
                else:
                    self.stdout.write(f"Could not geocode: {bank.name}")

            except Exception as e:
                self.stderr.write(f"Error processing {bank.name}: {str(e)}")