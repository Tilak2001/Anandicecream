"""Static configuration for Function Services hub and sub-categories."""

FUNCTION_HUB_CARDS = [
    {
        'slug': 'anand-ice-cream',
        'title': 'Anand Ice Cream',
        'description': 'Order ice cream for parties, birthdays & events',
        'icon': 'fa-ice-cream',
        'color': '#ffb74d',
        'bg': 'rgba(245,127,23,0.2)',
        'border': 'rgba(245, 158, 11, 0.35)',
        'image': 'images/anand-card.png',
        'external_url': '/ice-cream/',
    },
    {
        'slug': 'decoration',
        'title': 'Decoration',
        'description': 'Stage, floral & theme décor for every occasion',
        'icon': 'fa-wand-magic-sparkles',
        'color': '#f48fb1',
        'bg': 'rgba(194,24,91,0.2)',
        'border': 'rgba(244, 143, 177, 0.35)',
        'image': 'images/services-card.png',
    },
    {
        'slug': 'catering',
        'title': 'Catering',
        'description': 'Menus, thalis & live counters for your function',
        'icon': 'fa-utensils',
        'color': '#81c784',
        'bg': 'rgba(46,125,50,0.2)',
        'border': 'rgba(129, 199, 132, 0.35)',
        'image': 'images/goods-card.png',
    },
    {
        'slug': 'photography',
        'title': 'Photography',
        'description': 'Photos & videos to capture your special moments',
        'icon': 'fa-camera',
        'color': '#64b5f6',
        'bg': 'rgba(21,101,192,0.2)',
        'border': 'rgba(100, 181, 246, 0.35)',
        'image': 'images/places-card.png',
    },
]

DECORATION_EVENTS = [
    {'slug': 'marriage', 'title': 'Marriage', 'icon': 'fa-heart', 'description': 'Wedding mandap, stage & venue décor'},
    {'slug': 'haldi', 'title': 'Haldi', 'icon': 'fa-sun', 'description': 'Yellow-themed haldi ceremony setup'},
    {'slug': 'engagement', 'title': 'Engagement', 'icon': 'fa-gem', 'description': 'Ring ceremony & engagement stage décor'},
    {'slug': 'birthday', 'title': 'Birthday', 'icon': 'fa-cake-candles', 'description': 'Birthday party themes & balloon décor'},
    {'slug': 'baby-shower', 'title': 'Baby Shower', 'icon': 'fa-baby', 'description': 'Baby shower backdrop & table styling'},
    {'slug': 'naming-ceremony', 'title': 'Naming Ceremony', 'icon': 'fa-child', 'description': 'Cradle ceremony & traditional naming décor'},
]

CATERING_ITEMS = [
    {'slug': 'veg-thali', 'title': 'Veg Thali', 'icon': 'fa-leaf', 'description': 'Complete vegetarian meal packages'},
    {'slug': 'non-veg-thali', 'title': 'Non-Veg Thali', 'icon': 'fa-drumstick-bite', 'description': 'Chicken, mutton & fish thali menus'},
    {'slug': 'north-indian', 'title': 'North Indian', 'icon': 'fa-pepper-hot', 'description': 'Paneer, dal, roti & North Indian spreads'},
    {'slug': 'south-indian', 'title': 'South Indian', 'icon': 'fa-bowl-rice', 'description': 'Idli, dosa, sambar & South Indian meals'},
    {'slug': 'snacks-starters', 'title': 'Snacks & Starters', 'icon': 'fa-cookie-bite', 'description': 'Welcome snacks, chaat & starters'},
    {'slug': 'sweets-desserts', 'title': 'Sweets & Desserts', 'icon': 'fa-candy-cane', 'description': 'Mithai, ice cream & dessert counters'},
    {'slug': 'beverages', 'title': 'Beverages', 'icon': 'fa-mug-hot', 'description': 'Juices, tea, coffee & welcome drinks'},
    {'slug': 'live-counter', 'title': 'Live Counter', 'icon': 'fa-fire-burner', 'description': 'Live dosa, chaat, pasta & grill stations'},
]

PHOTOGRAPHY_TYPES = [
    {'slug': 'wedding', 'title': 'Wedding Photography', 'icon': 'fa-camera-retro', 'description': 'Full wedding day photo coverage'},
    {'slug': 'pre-wedding', 'title': 'Pre-Wedding', 'icon': 'fa-heart', 'description': 'Couple shoots at scenic locations'},
    {'slug': 'engagement', 'title': 'Engagement', 'icon': 'fa-ring', 'description': 'Engagement ceremony photography'},
    {'slug': 'birthday', 'title': 'Birthday', 'icon': 'fa-cake-candles', 'description': 'Birthday party photo & candid coverage'},
    {'slug': 'baby-shower', 'title': 'Baby Shower', 'icon': 'fa-baby', 'description': 'Maternity & baby shower albums'},
    {'slug': 'naming-ceremony', 'title': 'Naming Ceremony', 'icon': 'fa-child', 'description': 'Traditional naming ceremony photos'},
    {'slug': 'haldi', 'title': 'Haldi', 'icon': 'fa-sun', 'description': 'Haldi function photography & reels'},
    {'slug': 'videography', 'title': 'Videography', 'icon': 'fa-video', 'description': 'Cinematic films, highlights & drone shots'},
]

SEGMENT_CONFIG = {
    'decoration': {
        'title': 'Decoration Services',
        'subtitle': 'Choose your event type to browse décor providers',
        'items': DECORATION_EVENTS,
        'icon': 'fa-wand-magic-sparkles',
    },
    'catering': {
        'title': 'Catering Services',
        'subtitle': 'Select a menu type to find caterers in Karwar',
        'items': CATERING_ITEMS,
        'icon': 'fa-utensils',
    },
    'photography': {
        'title': 'Photography & Videography',
        'subtitle': 'Pick a package type to view photographers',
        'items': PHOTOGRAPHY_TYPES,
        'icon': 'fa-camera',
    },
}

VALID_SEGMENTS = set(SEGMENT_CONFIG.keys())
