from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.utils.text import slugify
import time

from .models import Service, ServiceCategory
from .function_services_config import (
    FUNCTION_HUB_CARDS,
    SEGMENT_CONFIG,
    VALID_SEGMENTS,
)
from django.db.models import Q

from .second_hand_config import SECOND_HAND_CATEGORIES, SECOND_HAND_CATEGORY_SLUGS, DEMO_ITEMS


def _category_slug_for_second_hand(public_slug):
    return f'sh-{public_slug}'


def _ensure_second_hand_categories():
    """Create category rows if missing (no separate migration required)."""
    for cfg in SECOND_HAND_CATEGORIES:
        ServiceCategory.objects.get_or_create(
            slug=_category_slug_for_second_hand(cfg['slug']),
            defaults={'name': cfg['name'], 'icon': cfg['icon']},
        )


def _get_second_hand_categories():
    _ensure_second_hand_categories()
    slugs = [_category_slug_for_second_hand(c['slug']) for c in SECOND_HAND_CATEGORIES]
    by_slug = {c.slug: c for c in ServiceCategory.objects.filter(slug__in=slugs)}
    ordered = []
    for cfg in SECOND_HAND_CATEGORIES:
        cat = by_slug.get(_category_slug_for_second_hand(cfg['slug']))
        if cat:
            ordered.append({'config': cfg, 'category': cat})
    return ordered


def _ensure_second_hand_demos():
    """Seed two approved demo listings if none exist yet."""
    if Service.objects.filter(service_type='second_hand', is_active=True).exists():
        return
    _ensure_second_hand_categories()
    by_slug = {
        c.slug: c
        for c in ServiceCategory.objects.filter(
            slug__in=[_category_slug_for_second_hand(x['slug']) for x in SECOND_HAND_CATEGORIES],
        )
    }
    for row in DEMO_ITEMS:
        if Service.objects.filter(slug=row['slug']).exists():
            continue
        cat = by_slug.get(_category_slug_for_second_hand(row['category_slug']))
        if not cat:
            continue
        Service.objects.create(
            title=row['title'],
            slug=row['slug'],
            category=cat,
            service_type='second_hand',
            description=row['description'],
            short_description=row['short_description'],
            price_text=row['price_text'],
            image_url=row['image_url'],
            provider_name=row['provider_name'],
            contact_phone=row['contact_phone'],
            location=row['location'],
            is_active=True,
            is_verified=True,
        )


def second_hand_list(request, category_slug=None):
    """Second Hand marketplace — main Goods & Services page."""
    _ensure_second_hand_categories()
    _ensure_second_hand_demos()

    items = Service.objects.filter(service_type='second_hand', is_active=True).select_related('category')
    current_category = None

    if category_slug:
        if category_slug not in SECOND_HAND_CATEGORY_SLUGS:
            raise Http404('Unknown category')
        current_category = get_object_or_404(
            ServiceCategory, slug=_category_slug_for_second_hand(category_slug),
        )
        items = items.filter(category=current_category)

    search = request.GET.get('search', '').strip()
    if search:
        items = items.filter(Q(title__icontains=search) | Q(description__icontains=search))

    categories = _get_second_hand_categories()

    context = {
        'items': items,
        'categories': categories,
        'item_count': items.count(),
        'current_category': current_category,
        'current_category_slug': category_slug,
        'search_query': search,
    }
    return render(request, 'services/second_hand_list.html', context)


def second_hand_add(request):
    """Submit a second-hand item for admin approval."""
    categories = _get_second_hand_categories()

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category_key = request.POST.get('category', '')
        description = request.POST.get('description', '').strip()
        price_text = request.POST.get('price_text', '').strip()
        location = request.POST.get('location', '').strip()
        provider_name = request.POST.get('provider_name', '').strip()
        contact_phone = request.POST.get('contact_phone', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        whatsapp_number = request.POST.get('whatsapp_number', '').strip()
        main_image = request.FILES.get('main_image')

        if not all([title, category_key, description, provider_name, contact_phone, location]):
            messages.error(request, 'Please fill in all required fields.')
        elif category_key not in SECOND_HAND_CATEGORY_SLUGS:
            messages.error(request, 'Please select a valid category.')
        else:
            cat = get_object_or_404(
                ServiceCategory, slug=_category_slug_for_second_hand(category_key),
            )
            base_slug = slugify(title) or 'item'
            slug = f'{base_slug}-{int(time.time())}'
            short_desc = description[:280] + '...' if len(description) > 280 else description

            Service.objects.create(
                title=title,
                slug=slug,
                category=cat,
                service_type='second_hand',
                description=description,
                short_description=short_desc,
                price_text=price_text or 'Negotiable',
                main_image=main_image,
                provider_name=provider_name,
                contact_phone=contact_phone,
                contact_email=contact_email,
                location=location,
                whatsapp_number=whatsapp_number,
                is_active=False,
                posted_by=request.user if request.user.is_authenticated else None,
            )
            messages.success(
                request,
                'Your item was submitted successfully! It will appear after admin approval.',
            )
            return redirect('services:goods_hub')

    return render(request, 'services/second_hand_add.html', {
        'categories': categories,
    })


def services_list(request):
    """List all services"""
    services = Service.objects.filter(is_active=True)
    categories = ServiceCategory.objects.all()
    
    # Filters
    category_slug = request.GET.get('category')
    service_type = request.GET.get('type')
    
    if category_slug:
        services = services.filter(category__slug=category_slug)
    if service_type:
        services = services.filter(service_type=service_type)
    
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'services/services_list.html', context)


def _get_segment_item(segment, subcategory):
    config = SEGMENT_CONFIG.get(segment)
    if not config:
        return None
    for item in config['items']:
        if item['slug'] == subcategory:
            return item
    return None


def function_services_hub(request):
    """Main Function Services landing with category cards."""
    context = {
        'hub_cards': FUNCTION_HUB_CARDS,
        'page_title': 'Function Services',
        'page_subtitle': 'Everything you need for weddings, parties & celebrations in Karwar',
    }
    return render(request, 'services/function_services_hub.html', context)


def function_services_section(request, segment):
    """Decoration, catering, or photography sub-category grid."""
    if segment not in VALID_SEGMENTS:
        raise Http404('Unknown function service category')
    config = SEGMENT_CONFIG[segment]
    context = {
        'segment': segment,
        'segment_config': config,
        'items': config['items'],
        'hub_url_name': 'services:function_hub',
    }
    return render(request, 'services/function_services_section.html', context)


def function_services_listings(request, segment, subcategory):
    """Listings for a specific event type or menu under Function Services."""
    if segment not in VALID_SEGMENTS:
        raise Http404('Unknown function service category')
    item = _get_segment_item(segment, subcategory)
    if not item:
        raise Http404('Unknown sub-category')

    services = Service.objects.filter(
        is_active=True,
        service_type='function_service',
        function_segment=segment,
        function_subcategory=subcategory,
    )

    context = {
        'segment': segment,
        'subcategory': subcategory,
        'subcategory_item': item,
        'segment_config': SEGMENT_CONFIG[segment],
        'services': services,
    }
    return render(request, 'services/function_services_listings.html', context)


def service_detail(request, slug):
    """Service detail page"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Increment views
    service.views_count += 1
    service.save(update_fields=['views_count'])
    
    # Related services
    related_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(id=service.id)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'services/service_detail.html', context)


def services_add(request):
    """Add a new service or second-hand item listing"""
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        service_type = request.POST.get('service_type')
        function_segment = request.POST.get('function_segment', '')
        function_subcategory = request.POST.get('function_subcategory', '')
        description = request.POST.get('description')
        price = request.POST.get('price')
        price_text = request.POST.get('price_text', '')
        provider_name = request.POST.get('provider_name')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email', '')
        location = request.POST.get('location')
        whatsapp_number = request.POST.get('whatsapp_number', '')
        
        main_image = request.FILES.get('main_image')
        
        # Validation
        if not (title and category_id and service_type and description and provider_name and contact_phone and location):
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                category = ServiceCategory.objects.get(id=category_id)
                # Create slug
                base_slug = slugify(title)
                if not base_slug:
                    base_slug = "item"
                slug = f"{base_slug}-{int(time.time())}"
                
                # short description from first 280 chars of description
                short_desc = description[:280] + '...' if len(description) > 280 else description
                
                # parsed price decimal
                parsed_price = None
                if price:
                    try:
                        parsed_price = float(price)
                    except ValueError:
                        pass
                
                service = Service.objects.create(
                    title=title,
                    slug=slug,
                    category=category,
                    service_type=service_type,
                    function_segment=function_segment,
                    function_subcategory=function_subcategory,
                    description=description,
                    short_description=short_desc,
                    price=parsed_price,
                    price_text=price_text,
                    main_image=main_image,
                    provider_name=provider_name,
                    contact_phone=contact_phone,
                    contact_email=contact_email,
                    location=location,
                    whatsapp_number=whatsapp_number,
                    is_active=False # default to inactive for admin review
                )
                
                messages.success(request, "Listing submitted successfully! It will be visible once reviewed and approved by the admin.")
                return redirect('services:goods_hub')
            except Exception as e:
                messages.error(request, f"Error saving listing: {str(e)}")
                
    categories = ServiceCategory.objects.all()
    service_types = Service.SERVICE_TYPE_CHOICES
    
    context = {
        'categories': categories,
        'service_types': service_types,
        'preset_service_type': request.GET.get('service_type', ''),
        'preset_function_segment': request.GET.get('function_segment', ''),
        'preset_function_subcategory': request.GET.get('function_subcategory', ''),
    }
    return render(request, 'services/service_form.html', context)
