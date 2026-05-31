"""Load default Karwar places and categories if the database is empty."""
from django.core.management.base import BaseCommand
from places.models import Place, PlaceCategory

DEFAULT_CATEGORIES = [
    {'slug': 'beach', 'name': 'Beaches', 'icon': '🏖️', 'description': 'Coastal beaches and seafronts'},
    {'slug': 'nature', 'name': 'Nature', 'icon': '🌿', 'description': 'Gardens, parks and riverside spots'},
    {'slug': 'heritage', 'name': 'Heritage', 'icon': '🏛️', 'description': 'Museums, forts and historic sites'},
    {'slug': 'adventure', 'name': 'Adventure', 'icon': '⛰️', 'description': 'Hills, waterfalls and viewpoints'},
]

DEFAULT_PLACES = [
    {
        'slug': 'rabindranath-tagore-beach',
        'name': 'Rabindranath Tagore Beach',
        'category': 'beach',
        'short_description': 'Serene beach named after Tagore — stunning sunsets and calm waters.',
        'description': 'Named after the Nobel laureate who was captivated by its beauty, this serene beach offers stunning sunsets, calm waters, and a peaceful escape.',
        'address': 'Karwar Town',
        'entry_fee': 'Free',
        'timings': 'Open 24 Hours',
        'best_time_to_visit': 'Oct - Mar',
        'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&h=400&fit=crop',
        'is_featured': True,
    },
    {
        'slug': 'karwar-beach',
        'name': 'Karwar Beach',
        'category': 'beach',
        'short_description': 'Main town beach with golden sand and evening promenade walks.',
        'description': 'The main beach of Karwar town, known for golden sand, gentle waves, and a vibrant atmosphere.',
        'address': 'Karwar Town',
        'entry_fee': 'Free',
        'timings': 'Open 24 Hours',
        'best_time_to_visit': 'Nov - Feb',
        'image_url': 'https://images.unsplash.com/photo-1519046904884-53103b34b206?w=600&h=400&fit=crop',
        'is_featured': True,
    },
    {
        'slug': 'devbag-beach',
        'name': 'Devbag Beach',
        'category': 'beach',
        'short_description': 'Pristine beach at Kali River and Arabian Sea confluence.',
        'description': 'Famous for water sports, dolphin sightings, and the stunning Devbag sangam point.',
        'address': 'Devbag',
        'entry_fee': 'Free',
        'timings': 'Open 24 Hours',
        'best_time_to_visit': 'Oct - Mar',
        'image_url': 'https://images.unsplash.com/photo-1468413253725-0d5181091126?w=600&h=400&fit=crop',
        'is_featured': True,
    },
    {
        'slug': 'tilmati-beach',
        'name': 'Tilmati Beach',
        'category': 'beach',
        'short_description': 'Secluded black-sand beach surrounded by green hills.',
        'description': 'A serene and secluded beach perfect for peace and solitude.',
        'address': 'Tilmati Village',
        'entry_fee': 'Free',
        'timings': 'Open 24 Hours',
        'best_time_to_visit': 'Oct - Mar',
        'image_url': 'https://images.unsplash.com/photo-1476673160081-cf065607f449?w=600&h=400&fit=crop',
    },
    {
        'slug': 'kali-river-garden',
        'name': 'Kali River Garden',
        'category': 'nature',
        'short_description': 'Landscaped garden on the Kali River with boating views.',
        'description': 'Beautiful garden along the Kali River with boating and views of the river meeting the sea.',
        'address': 'Near Kali Bridge',
        'entry_fee': '₹20',
        'timings': '9 AM - 6 PM',
        'best_time_to_visit': 'Oct - Mar',
        'image_url': 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=600&h=400&fit=crop',
    },
    {
        'slug': 'nirmith-park',
        'name': 'Nirmith Park',
        'category': 'nature',
        'short_description': 'Family park with gardens and play areas.',
        'description': 'Recreational park with gardens, play areas, and shaded walking paths.',
        'address': 'Karwar Town',
        'entry_fee': '₹10',
        'timings': '8 AM - 7 PM',
        'best_time_to_visit': 'Year Round',
        'image_url': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&h=400&fit=crop',
    },
    {
        'slug': 'golari-falls',
        'name': 'Golari Falls, Todur',
        'category': 'adventure',
        'short_description': 'Multi-tiered waterfall in the Western Ghats — best in monsoon.',
        'description': 'Magnificent waterfall nestled in the Western Ghats; breathtaking during monsoon.',
        'address': 'Todur Village',
        'entry_fee': 'Free',
        'timings': '8 AM - 5 PM',
        'best_time_to_visit': 'Jul - Nov',
        'image_url': 'https://images.unsplash.com/photo-1482938289607-e9573fc25ebb?w=600&h=400&fit=crop',
        'is_featured': True,
    },
    {
        'slug': 'sirve-gudda',
        'name': 'Sirve Gudda',
        'category': 'adventure',
        'short_description': 'Hilltop viewpoint with panoramic sea and town views.',
        'description': 'Rocky hilltop with 360-degree views — ideal for sunsets and photography.',
        'address': 'Karwar Hills',
        'entry_fee': 'Free',
        'timings': '6 AM - 6 PM',
        'best_time_to_visit': 'Oct - Feb',
        'image_url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&h=400&fit=crop',
    },
    {
        'slug': 'guddali',
        'name': 'Guddali',
        'category': 'adventure',
        'short_description': 'Picturesque village near Karwar surrounded by lush green hills.',
        'description': 'A picturesque village near Karwar surrounded by lush green hills and traditional Konkani culture. An offbeat destination for those seeking authentic rural experiences.',
        'address': 'Near Karwar',
        'entry_fee': 'Free',
        'timings': 'Open 24 Hours',
        'best_time_to_visit': 'Sep - Feb',
        'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop',
    },
    {
        'slug': 'rock-garden',
        'name': 'Rock Garden',
        'category': 'heritage',
        'short_description': 'Artistic rock sculptures overlooking the coast.',
        'description': 'Garden with creative rock formations and stone sculptures overlooking the sea.',
        'address': 'Karwar Coast',
        'entry_fee': '₹15',
        'timings': '9 AM - 6 PM',
        'best_time_to_visit': 'Year Round',
        'image_url': 'https://images.unsplash.com/photo-1502472584811-0a2f2feb8968?w=600&h=400&fit=crop',
    },
    {
        'slug': 'karwar-ship-museum',
        'name': 'Karwar Ship Museum',
        'category': 'heritage',
        'short_description': 'Naval heritage museum aboard a decommissioned warship.',
        'description': 'Learn about India\'s maritime history and Karwar\'s naval importance.',
        'address': 'Karwar Port',
        'entry_fee': '₹30',
        'timings': '10 AM - 5 PM',
        'best_time_to_visit': 'Year Round',
        'image_url': 'https://images.unsplash.com/photo-1569263979104-865ab7cd8d13?w=600&h=400&fit=crop',
        'is_featured': True,
    },
]


class Command(BaseCommand):
    help = 'Load default place categories and destinations for Karwar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Add missing places even if some already exist',
        )

    def handle(self, *args, **options):
        force = options['force']
        if Place.objects.exists() and not force:
            self.stdout.write(self.style.WARNING(
                'Places already exist. Run with --force to add any missing defaults.'
            ))
            return

        categories = {}
        for cat_data in DEFAULT_CATEGORIES:
            cat, _ = PlaceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'description': cat_data['description'],
                },
            )
            categories[cat.slug] = cat

        created = 0
        for place_data in DEFAULT_PLACES:
            cat_slug = place_data.pop('category')
            slug = place_data['slug']
            if Place.objects.filter(slug=slug).exists():
                continue
            Place.objects.create(category=categories[cat_slug], **place_data)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Categories: {len(categories)}, new places added: {created}'
        ))
