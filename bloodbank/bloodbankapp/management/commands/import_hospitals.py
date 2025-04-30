from django.core.management.base import BaseCommand
from bloodbank.utils.osm_utils import fetch_osm_hospitals
from bloodbankapp.models import Hospital
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Import hospitals from OpenStreetMap'

    def add_arguments(self, parser):
        parser.add_argument(
            '--location',
            type=str,
            default='Mumbai',
            help='City/region to search for hospitals'
        )
        parser.add_argument(
            '--type',
            type=str,
            default=None,
            help='Filter by hospital type (e.g., blood_bank)'
        )

    def handle(self, *args, **options):
        location = options['location']
        hospital_type = options['type']

        filters = {}
        if hospital_type:
            filters['healthcare'] = hospital_type

        hospitals = fetch_osm_hospitals(location, filters)

        if not hospitals:
            self.stdout.write(self.style.ERROR('No hospitals found!'))
            return

        created_count = 0
        for hospital in hospitals:
            _, created = Hospital.objects.update_or_create(
                osm_id=hospital['osm_id'],
                defaults={
                    'name': hospital['name'],
                    'latitude': hospital['latitude'],
                    'longitude': hospital['longitude'],
                    'address': hospital['address'],
                    'hospital_type': hospital['type'],
                    'phone': hospital['phone']
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed {len(hospitals)} hospitals. "
                f"Created {created_count} new entries."
            )
        )

    def handle(self, *args, **options):
        hospitals = fetch_osm_hospitals(options['location'])

        for hospital in hospitals:
            # Clean None values
            hospital['address'] = hospital.get('address') or "Address not available"
            hospital['phone'] = hospital.get('phone') or "Not listed"

            Hospital.objects.update_or_create(
                osm_id=hospital['osm_id'],
                defaults={
                    'name': hospital['name'],
                    'latitude': hospital['latitude'],
                    'longitude': hospital['longitude'],
                    'address': hospital['address'],
                    'phone': hospital['phone'],
                    'hospital_type': hospital['type']
                }
            )