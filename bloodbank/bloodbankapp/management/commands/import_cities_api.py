import csv
from django.core.management.base import BaseCommand
from bloodbankapp.models import City


class Command(BaseCommand):
    help = 'Import cities from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        # Correct way to access the file path argument
        file_path = options['file_path']  # This is the critical fix

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                cities = [
                    City(
                        name=row['name'],
                        state=row['state'],
                        latitude=float(row['latitude']),
                        longitude=float(row['longitude'])
                    )
                    for row in reader
                ]
                City.objects.bulk_create(cities)
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(cities)} cities'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing required column in CSV: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing cities: {str(e)}'))