from django.core.management.base import BaseCommand

from vendors.models import Category


class Command(BaseCommand):
    help = "Seed default vendor categories into the database"

    def handle(self, *args, **options):
        categories = [
            {"name": "Plumber", "icon": "🔧"},
            {"name": "Electrician", "icon": "⚡"},
            {"name": "Grocery", "icon": "🛒"},
            {"name": "Tutor", "icon": "📚"},
            {"name": "Mechanic", "icon": "🔩"},
            {"name": "Salon", "icon": "💇"},
            {"name": "Doctor", "icon": "🏥"},
            {"name": "Restaurant", "icon": "🍽️"},
        ]

        for cat in categories:
            obj, created = Category.objects.get_or_create(
                name=cat["name"], defaults={"icon": cat["icon"]}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created category: {cat['name']}")
                )
            else:
                self.stdout.write(f"⊘ Category already exists: {cat['name']}")

        self.stdout.write(
            self.style.SUCCESS("\n✓ Seeding completed successfully!")
        )
