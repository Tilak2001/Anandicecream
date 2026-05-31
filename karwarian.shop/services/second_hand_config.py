"""Second-hand marketplace categories (ported from WordPress plugin concept)."""

SECOND_HAND_CATEGORIES = [
    {'slug': 'electronics', 'name': 'Electronics', 'icon': '📱', 'description': 'Phones, laptops, TVs & gadgets'},
    {'slug': 'furniture', 'name': 'Furniture', 'icon': '🛋️', 'description': 'Chairs, tables, beds & home furniture'},
    {'slug': 'vehicles', 'name': 'Vehicles', 'icon': '🚗', 'description': 'Bikes, cars & auto parts'},
    {'slug': 'home-appliances', 'name': 'Home Appliances', 'icon': '🔌', 'description': 'Fridge, washing machine, AC & more'},
    {'slug': 'fashion', 'name': 'Fashion', 'icon': '👕', 'description': 'Clothing, footwear & accessories'},
    {'slug': 'books-sports', 'name': 'Books & Sports', 'icon': '📚', 'description': 'Books, gym gear & outdoor items'},
    {'slug': 'other', 'name': 'Other', 'icon': '📦', 'description': 'Everything else'},
]

SECOND_HAND_CATEGORY_SLUGS = {c['slug'] for c in SECOND_HAND_CATEGORIES}

DEMO_ITEMS = [
    {
        'slug': 'used-office-chair-karwar',
        'title': 'Used Office Chair (Mesh)',
        'short_description': 'Comfortable mesh chair. Minor wear on armrests. Pickup in Karwar.',
        'description': 'Comfortable mesh office chair. Minor wear on armrests. Ideal for home office. Pickup only in Karwar town.',
        'price_text': '₹2,200',
        'location': 'Karwar Town',
        'provider_name': 'Ramesh K',
        'contact_phone': '9876500001',
        'category_slug': 'furniture',
        'image_url': 'https://images.unsplash.com/photo-1580480057503-1114c6f9d1c5?w=600&h=400&fit=crop',
    },
    {
        'slug': 'mountain-bike-26-karwar',
        'title': 'Mountain Bike 26"',
        'short_description': 'Single owner, serviced last month. Tyres in good condition.',
        'description': 'Mountain bike 26 inch wheels. Single owner, serviced last month. Tyres and brakes in good condition.',
        'price_text': '₹8,500',
        'location': 'Baad, Karwar',
        'provider_name': 'Suresh Naik',
        'contact_phone': '9876500002',
        'category_slug': 'vehicles',
        'image_url': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=600&h=400&fit=crop',
    },
]
