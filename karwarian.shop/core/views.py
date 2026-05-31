from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import SiteStatistics, BusTiming, ContactMessage, MatrimonyProfile


def home(request):
    """Home page view"""
    try:
        stats = SiteStatistics.objects.first()
    except SiteStatistics.DoesNotExist:
        stats = None
    
    context = {
        'stats': stats,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'core/contact.html')


def bus_timings(request):
    """Bus timings page view"""
    timings = BusTiming.objects.filter(is_active=True)
    
    # Get unique locations for filtering
    from_locations = BusTiming.objects.filter(is_active=True).values_list('from_location', flat=True).distinct()
    to_locations = BusTiming.objects.filter(is_active=True).values_list('to_location', flat=True).distinct()
    
    # Apply filters if provided
    from_filter = request.GET.get('from')
    to_filter = request.GET.get('to')
    
    if from_filter:
        timings = timings.filter(from_location=from_filter)
    if to_filter:
        timings = timings.filter(to_location=to_filter)
    
    context = {
        'timings': timings,
        'from_locations': from_locations,
        'to_locations': to_locations,
        'selected_from': from_filter,
        'selected_to': to_filter,
    }
    return render(request, 'core/bus_timings.html', context)


def cricket_score(request):
    """Cricket score page view - Live cricket scores"""
    return render(request, 'core/cricket_score.html')


def matrimony_list(request):
    """Matrimony profiles listing page — members only."""
    if not request.user.is_authenticated:
        return render(request, 'core/matrimony_signin.html', {
            'next': request.get_full_path() or reverse('matrimony_list'),
        })

    profiles = MatrimonyProfile.objects.filter(is_approved=True, is_active=True)
    
    # Filter by caste if provided
    caste_filter = request.GET.get('caste')
    if caste_filter and caste_filter != 'all':
        profiles = profiles.filter(caste=caste_filter)
    
    # Get unique castes for filter dropdown
    castes = MatrimonyProfile.CASTE_CHOICES
    
    # Count profiles
    total_profiles = profiles.count()
    
    context = {
        'profiles': profiles,
        'castes': castes,
        'selected_caste': caste_filter,
        'total_profiles': total_profiles,
    }
    return render(request, 'core/matrimony_list.html', context)


@login_required(login_url='user_login')
def matrimony_detail(request, profile_id):
    """Full matrimony profile with large photo and all details."""
    profile = get_object_or_404(
        MatrimonyProfile,
        pk=profile_id,
        is_approved=True,
        is_active=True,
    )
    context = {
        'profile': profile,
    }
    return render(request, 'core/matrimony_detail.html', context)


@login_required(login_url='user_login')
def matrimony_add(request):
    """Add matrimony profile - user submission"""
    if request.method == 'POST':
        profile = MatrimonyProfile(
            full_name=request.POST.get('full_name'),
            father_name=request.POST.get('father_name'),
            age=int(request.POST.get('age')),
            gender=request.POST.get('gender'),
            height=request.POST.get('height', ''),
            caste=request.POST.get('caste'),
            qualification=request.POST.get('qualification'),
            occupation=request.POST.get('occupation', ''),
            contact_phone=request.POST.get('contact_phone', ''),
            contact_email=request.POST.get('contact_email', ''),
            address=request.POST.get('address', ''),
            additional_info=request.POST.get('additional_info', ''),
            is_approved=False,
        )
        if request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
        profile.save()
        messages.success(request, 'Your profile has been submitted successfully! It will be visible after admin approval.')
        return redirect('matrimony_list')
    
    return redirect('matrimony_list')

