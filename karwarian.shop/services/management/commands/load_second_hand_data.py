"""Seed second-hand categories and two demo listings in Karwar."""
from django.core.management.base import BaseCommand
from services.models import Service, ServiceCategory
from services.second_hand_config import SECOND_HAND_CATEGORIES, DEMO_ITEMS


class Command(BaseCommand):
    help = 'Create second-hand categories and two approved demo listings'

    def handle(self, *args, **options):
        categories = {}
        for cat in SECOND_HAND_CATEGORIES:
            obj, created = ServiceCategory.objects.get_or_create(
                slug=f"sh-{cat['slug']}",
                defaults={
                    'name': cat['name'],
                    'icon': cat['icon'],
                },
            )
            categories[cat['slug']] = obj
            if created:
                self.stdout.write(f'  + category: {obj.name}')

        for row in DEMO_ITEMS:
            if Service.objects.filter(slug=row['slug']).exists():
                continue
            item = row.copy()
            category_slug = item.pop('category_slug')
            cat = categories[category_slug]
            Service.objects.create(
                category=cat,
                service_type='second_hand',
                is_active=True,
                is_verified=True,
                **item,
            )
            self.stdout.write(self.style.SUCCESS(f'  + demo item: {row["title"]}'))

        self.stdout.write(self.style.SUCCESS('Second-hand data ready.'))
