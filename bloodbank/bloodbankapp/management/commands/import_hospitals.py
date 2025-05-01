from django.core.management.base import BaseCommand
import pandas as pd
from bloodbankapp.models import Hospital


class Command(BaseCommand):
    help = 'Import hospitals with field length validation'

    def handle(self, *args, **options):
        csv_path = 'bloodbankapp/data/imports/hospitals.csv'

        try:
            df = pd.read_csv(csv_path)

            # Get max lengths from model
            field_max_lengths = {
                'name': 100,
                'address': 200,
                'phone': 20,
                'email': 100,
                'hospital_type': 50,
                'state': 50,
                'district': 50,
                'pincode': 10,
                'website': 200
            }

            hospitals = []
            skipped = 0

            for _, row in df.iterrows():
                # Prepare data with length validation
                hospital_data = {
                    'name': self._clean_field(row['Name'], field_max_lengths['name']),
                    'address': self._clean_field(row['Address'], field_max_lengths['address']),
                    'phone': self._clean_field(row['telephone'], field_max_lengths['phone']),
                    'email': self._clean_field(row['Email'], field_max_lengths['email']) if pd.notna(
                        row['Email']) else '',
                    'hospital_type': self._clean_field(row['Hospital_Type'], field_max_lengths['hospital_type']),
                    'state': self._clean_field(row['state'], field_max_lengths['state']),
                    'district': self._clean_field(row['district'], field_max_lengths['district']),
                    'pincode': self._clean_field(row['pincode'], field_max_lengths['pincode']),
                    'website': self._clean_field(row['website'], field_max_lengths['website']) if pd.notna(
                        row['website']) else '',
                    'latitude': self._clean_coordinate(row['latitude']),
                    'longitude': self._clean_coordinate(row['Longitude'])
                }

                # Skip if required fields are invalid
                if not all([hospital_data['name'], hospital_data['address'], hospital_data['phone']]):
                    skipped += 1
                    continue

                hospitals.append(Hospital(**hospital_data))

            # Import in batches of 500 for better performance
            batch_size = 500
            for i in range(0, len(hospitals), batch_size):
                Hospital.objects.bulk_create(hospitals[i:i + batch_size])

            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported {len(hospitals)} hospitals\n'
                f'Skipped {skipped} invalid records\n'
                f'Sample imported record:\n'
                f'Name: {hospitals[0].name}\n'
                f'Phone: {hospitals[0].phone}'
            ))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Import failed: {str(e)}'))

    def _clean_field(self, value, max_length):
        """Clean and truncate string fields"""
        if pd.isna(value):
            return ''
        value = str(value).strip()
        return value[:max_length]

    def _clean_coordinate(self, coord):
        """Clean coordinate values"""
        if pd.isna(coord):
            return None
        try:
            return float(str(coord).replace('°', '').replace("'", "").replace('"', ''))
        except ValueError:
            return None