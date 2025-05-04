import csv
from django.core.management.base import BaseCommand
from bloodbankapp.models import BloodBank


class Command(BaseCommand):
    help = 'Imports blood bank data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as csvfile:
                # Read first line to verify structure
                first_line = csvfile.readline()
                if 'Blood Bank Name' not in first_line:
                    raise ValueError("CSV missing required 'Blood Bank Name' column")

                # Return to start of file
                csvfile.seek(0)

                reader = csv.DictReader(
                    csvfile,
                    skipinitialspace=True,  # Handle spaces after commas
                    restval=None  # Default value for missing columns
                )

                success_count = 0
                error_count = 0

                for i, row in enumerate(reader, 1):
                    # Skip empty rows
                    if not row or not row.get('Blood Bank Name'):
                        continue

                    try:
                        # Clean and prepare data
                        cleaned_row = {
                            'name': row['Blood Bank Name'].strip(),
                            'state': row.get('State', '').strip(),
                            'district': row.get('District', '').strip(),
                            'address': row.get('Address', '').replace('\n', ', ').strip(),
                            'pincode': row.get('Pincode', '').strip(),

                            'mobile': row.get('Mobile', '').strip(),
                            'email': row.get('Email', '').strip().lower(),
                            'website': row.get('Website', '').strip().lower(),
                            'category': row.get('Category', '').strip(),
                            'blood_component_available': row.get('Blood Component Available',
                                                                 '').strip().upper() == 'YES',
                            'latitude': self._clean_float(row.get('Latitude')),
                            'longitude': self._clean_float(row.get('Longitude'))
                        }

                        # Create record
                        BloodBank.objects.create(**cleaned_row)
                        success_count += 1

                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f"Row {i}: Error - {str(e)}. Data: {row}")
                        )

                # Summary report
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nImport complete. Success: {success_count}, Errors: {error_count}"
                    )
                )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: File not found at {csv_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))

    def _clean_float(self, value):
        """Helper to safely convert to float or return None"""
        if not value or str(value).strip() == '':
            return None
        try:
            return float(str(value).strip())
        except ValueError:
            return None