# bloodbankapp/management/commands/remove_duplicate_hospitals.py
from django.core.management.base import BaseCommand
from django.db.models import Count
from bloodbankapp.models import Hospital  # Changed from 'your_app'


class Command(BaseCommand):
    help = 'Permanently removes duplicate hospitals based on name and address'

    def handle(self, *args, **options):
        # Step 1: Find duplicates (group by name + address)
        duplicates = (
            Hospital.objects.values('name', 'address')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        if not duplicates:
            self.stdout.write(self.style.SUCCESS('No duplicates found!'))
            return

        self.stdout.write(f"Found {len(duplicates)} duplicate groups...")

        # Step 2: Process each duplicate group
        total_deleted = 0
        for group in duplicates:
            # Get all duplicates for this group
            duplicates_qs = Hospital.objects.filter(
                name=group['name'],
                address=group['address']
            )

            # Get IDs to keep (oldest record) and delete others
            keeper = duplicates_qs.order_by('id').first()
            count = duplicates_qs.exclude(id=keeper.id).delete()[0]
            total_deleted += count

            self.stdout.write(
                f"Deleted {count} duplicates of '{group['name']}' at {group['address']}'"
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {total_deleted} duplicate hospitals!')
        )