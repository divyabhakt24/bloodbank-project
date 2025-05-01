from django.core.management.base import BaseCommand
import pandas as pd
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Verify hospital CSV file structure before import'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file to verify'
        )

    def handle(self, *args, **options):
        csv_path = options['csv_file']

        # Try to locate the file
        possible_paths = [
            csv_path,  # As provided
            os.path.join(settings.BASE_DIR, csv_path),  # Relative to project
            os.path.join('bloodbankapp/data/imports', os.path.basename(csv_path))  # Specific to your structure
        ]

        found_path = None
        for path in possible_paths:
            if os.path.exists(path):
                found_path = path
                break

        if not found_path:
            self.stderr.write(f"Error: File not found at any of these locations:\n" +
                              "\n".join(f" - {p}" for p in possible_paths))
            return

        try:
            # Read CSV file
            df = pd.read_csv(found_path)
            self.stdout.write(f"Successfully loaded {len(df)} records from:\n{found_path}")

            # Check required columns
            required_columns = {
                'name': ['Name', 'name', 'hospital_name'],
                'address': ['Address', 'address', 'location'],
                'phone': ['telephone', 'phone', 'contact_number']
            }

            # Find matching columns
            column_mapping = {}
            for field, alternatives in required_columns.items():
                for col in alternatives:
                    if col in df.columns:
                        column_mapping[field] = col
                        break

            # Report results
            self.stdout.write("\nColumn mapping:")
            for field, col in column_mapping.items():
                self.stdout.write(f"  {field} → {col}")

            # Check for missing required fields
            missing = [field for field in required_columns if field not in column_mapping]
            if missing:
                self.stderr.write(f"\nERROR: Missing required fields: {', '.join(missing)}")
                self.stdout.write("\nAvailable columns in CSV:")
                self.stdout.write(", ".join(df.columns))
            else:
                self.stdout.write(self.style.SUCCESS("\n✓ All required fields present"))

            # Show sample data
            self.stdout.write("\nFirst 3 rows of data:")
            self.stdout.write(str(df.head(3)))

        except Exception as e:
            self.stderr.write(f"Error verifying CSV: {str(e)}")