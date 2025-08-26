import csv
import os
from django.core.management.base import BaseCommand
from apps.tourism.models import TouristSpot, Category, Location

class Command(BaseCommand):
    help = 'Load tourist spots from CSV file'

    def handle(self, *args, **options):
        # Get the project root (directory containing manage.py's parent)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"Project root: {project_root}")

        # Construct the full path to the CSV file relative to project root
        csv_path = os.path.join(project_root, 'data', '../../../../../shared/static/tourism_reported_spots_albay.csv')
        print(f"Looking for CSV at: {csv_path}")

        # Check if the file exists
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at: {csv_path}'))
            # For debugging, print the directory contents
            data_dir = os.path.join(project_root, 'data')
            if os.path.exists(data_dir):
                print(f"Contents of {data_dir}: {os.listdir(data_dir)}")
            else:
                print(f"Data directory not found at: {data_dir}")
            return

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Create or get Category
                    category, _ = Category.objects.get_or_create(name=row['category_name'])

                    # Create or get Location
                    location, _ = Location.objects.get_or_create(
                        name=row['location_name'],
                        region=row['region'],
                        province=row['province']
                    )

                    # Create or update TouristSpot
                    TouristSpot.objects.update_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'category': category,
                            'location': location,
                            'image': row['image'],
                            'embed_link': row['embed_link'],
                            'website_link': row['website_link'],
                            'is_featured': row['is_featured'].lower() == 'true',
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Successfully loaded tourist spots'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))