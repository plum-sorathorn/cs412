from django.core.management.base import BaseCommand
from project.models import CuisineType

class Command(BaseCommand):
    help = 'Seeds the database with standard cuisine types matching Google Places API'

    def handle(self, *args, **kwargs):
        # Google Places types DO NOT include `_restaurant`
        cuisines = [
            {"name": "Japanese", "api": "japanese"},
            {"name": "Chinese", "api": "chinese"},
            {"name": "Mexican", "api": "mexican"},
            {"name": "Italian", "api": "italian"},
            {"name": "Thai", "api": "thai"},
            {"name": "Indian", "api": "indian"},
            {"name": "French", "api": "french"},
            {"name": "American", "api": "american"},
            {"name": "Pizza", "api": "pizza"},
            {"name": "Cafe", "api": "cafe"},
            {"name": "Steakhouse", "api": "steakhouse"},
            {"name": "Seafood", "api": "seafood"},
            {"name": "Sushi", "api": "sushi"},
        ]

        for item in cuisines:
            obj, created = CuisineType.objects.get_or_create(
                api_identifier=item['api'],
                defaults={'name': item['name']}
            )
            if created:
                self.stdout.write(f"Added: {item['name']}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded cuisines'))
