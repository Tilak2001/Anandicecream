from .models import SiteStatistics


def site_statistics(request):
    """Make site statistics available to all templates"""
    try:
        stats = SiteStatistics.objects.first()
    except SiteStatistics.DoesNotExist:
        stats = None
    
    return {
        'site_stats': stats
    }
