from django.shortcuts import render, get_object_or_404
from .models import News, NewsCategory


def news_list(request):
    """List all news"""
    news = News.objects.filter(is_published=True)
    categories = NewsCategory.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        news = news.filter(category__slug=category_slug)
    
    context = {
        'news_list': news,
        'categories': categories,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, slug):
    """News detail page"""
    news = get_object_or_404(News, slug=slug, is_published=True)
    
    # Increment views
    news.views_count += 1
    news.save(update_fields=['views_count'])
    
    # Related news
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/news_detail.html', context)
