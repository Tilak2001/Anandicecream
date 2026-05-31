from django.shortcuts import render, get_object_or_404
from .models import Place, PlaceCategory


def places_list(request):
    """List all places"""
    places = Place.objects.filter(is_active=True)
    categories = PlaceCategory.objects.all()
    
    # Filter by search query
    search_query = request.GET.get('search')
    if search_query:
        places = places.filter(name__icontains=search_query) | places.filter(description__icontains=search_query)
    
    context = {
        'places': places,
        'categories': categories,
        'search_query': search_query,
        'current_category': None,
    }
    return render(request, 'places/places_list.html', context)


def places_by_category(request, slug):
    """List places by category"""
    category = get_object_or_404(PlaceCategory, slug=slug)
    places = Place.objects.filter(category=category, is_active=True)
    categories = PlaceCategory.objects.all()
    
    context = {
        'places': places,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'places/places_list.html', context)


def place_detail(request, slug):
    """Place detail page"""
    place = get_object_or_404(Place, slug=slug, is_active=True)
    
    # Increment views count
    place.views_count += 1
    place.save(update_fields=['views_count'])
    
    # Get related places from same category
    related_places = Place.objects.filter(
        category=place.category,
        is_active=True
    ).exclude(id=place.id)[:3]
    
    context = {
        'place': place,
        'related_places': related_places,
    }
    return render(request, 'places/place_detail.html', context)
