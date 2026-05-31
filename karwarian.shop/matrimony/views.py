from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MatrimonyProfile


def matrimony_list(request):
    """List matrimony profiles"""
    profiles = MatrimonyProfile.objects.filter(is_active=True, is_verified=True)
    
    # Filters
    gender = request.GET.get('gender')
    if gender:
        profiles = profiles.filter(gender=gender)
    
    context = {
        'profiles': profiles,
    }
    return render(request, 'matrimony/profile_list.html', context)


@login_required
def profile_detail(request, pk):
    """View profile detail"""
    profile = get_object_or_404(MatrimonyProfile, pk=pk, is_active=True, is_verified=True)
    
    # Increment views
    profile.views_count += 1
    profile.save(update_fields=['views_count'])
    
    context = {
        'profile': profile,
    }
    return render(request, 'matrimony/profile_detail.html', context)


@login_required
def my_profile(request):
    """User's own matrimony profile"""
    try:
        profile = request.user.matrimony_profile
    except MatrimonyProfile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile,
    }
    return render(request, 'matrimony/my_profile.html', context)
