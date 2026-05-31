"""
Unified Admin Dashboard for Karwarian.shop
Manages: Cricket Live Scores, Ice Cream Orders, News Posts, Matrimony Profiles
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from core.models import CricketMatch, Innings, ContactMessage, MatrimonyProfile
from icecream.models import Order
from news.models import News, NewsCategory


ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '631176'


def dashboard_login_required(view_func):
    """Decorator to check if user is logged into the dashboard"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('dashboard_admin'):
            return redirect('dashboard_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def dashboard_login(request):
    """Dashboard login page"""
    if request.session.get('dashboard_admin'):
        return redirect('dashboard_home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['dashboard_admin'] = True
            request.session['dashboard_username'] = username
            return redirect('dashboard_home')
        else:
            error = 'Invalid username or password'
    
    return render(request, 'dashboard/login.html', {'error': error})


def dashboard_logout(request):
    """Dashboard logout"""
    request.session.pop('dashboard_admin', None)
    request.session.pop('dashboard_username', None)
    return redirect('dashboard_login')


@dashboard_login_required
def dashboard_home(request):
    """Main dashboard overview"""
    # Ice cream stats
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    confirmed_orders = Order.objects.filter(status='confirmed').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    total_revenue = sum(float(o.total_amount) for o in Order.objects.all())
    
    # Cricket stats
    live_matches = CricketMatch.objects.filter(status='live', is_active=True).count()
    total_matches = CricketMatch.objects.filter(is_active=True).count()
    
    # News stats
    total_news = News.objects.filter(is_published=True).count()
    
    # Contact messages
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # Recent orders
    recent_orders = Order.objects.all()[:5]
    
    # Live matches
    live_match_list = CricketMatch.objects.filter(status='live', is_active=True)
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'delivered_orders': delivered_orders,
        'total_revenue': total_revenue,
        'live_matches': live_matches,
        'total_matches': total_matches,
        'total_news': total_news,
        'unread_messages': unread_messages,
        'recent_orders': recent_orders,
        'live_match_list': live_match_list,
    }
    return render(request, 'dashboard/home.html', context)


# ========== CRICKET MANAGEMENT ==========

@dashboard_login_required
def cricket_list(request):
    """List all cricket matches - WordPress plugin style dashboard"""
    matches = CricketMatch.objects.filter(is_active=True)
    total = matches.count()
    live_count = matches.filter(status='live').count()
    upcoming_count = matches.filter(status='upcoming').count()
    completed_count = matches.filter(status='completed').count()
    
    context = {
        'matches': matches,
        'total': total,
        'live_count': live_count,
        'upcoming_count': upcoming_count,
        'completed_count': completed_count,
    }
    return render(request, 'dashboard/cricket_list.html', context)


@dashboard_login_required
def cricket_add(request):
    """Add a new cricket match"""
    if request.method == 'POST':
        match = CricketMatch.objects.create(
            series_name=request.POST.get('series_name', 'Karwar District League'),
            team1_name=request.POST.get('team1_name'),
            team2_name=request.POST.get('team2_name'),
            venue=request.POST.get('venue', ''),
            match_date=request.POST.get('match_date'),
            overs_limit=int(request.POST.get('overs_limit', 20)),
            status=request.POST.get('status', 'upcoming'),
        )
        # Auto-create both innings with default scorecard
        match.ensure_innings()
        return redirect('cricket_list')
    return render(request, 'dashboard/cricket_form.html', {'action': 'Add'})


@dashboard_login_required
def cricket_edit(request, match_id):
    """Edit cricket match details"""
    match = get_object_or_404(CricketMatch, id=match_id)
    if request.method == 'POST':
        match.series_name = request.POST.get('series_name', match.series_name)
        match.team1_name = request.POST.get('team1_name', match.team1_name)
        match.team2_name = request.POST.get('team2_name', match.team2_name)
        match.venue = request.POST.get('venue', match.venue)
        match.overs_limit = int(request.POST.get('overs_limit', match.overs_limit))
        match.status = request.POST.get('status', match.status)
        match.save()
        return redirect('cricket_list')
    return render(request, 'dashboard/cricket_form.html', {'action': 'Edit', 'match': match})


@dashboard_login_required
def cricket_live_update(request, match_id):
    """Full scorecard live update — matches WordPress plugin layout"""
    match = get_object_or_404(CricketMatch, id=match_id)
    match.ensure_innings()
    
    innings_num = int(request.GET.get('innings', 1))
    innings = get_object_or_404(Innings, match=match, innings_number=innings_num)
    
    if request.method == 'POST':
        # Score & Status
        innings.batting_team = request.POST.get('batting_team', innings.batting_team)
        innings.total_runs = int(request.POST.get('total_runs', innings.total_runs) or 0)
        innings.wickets = int(request.POST.get('wickets', innings.wickets) or 0)
        innings.overs = request.POST.get('overs', innings.overs)
        innings.extras = int(request.POST.get('extras', innings.extras) or 0)
        innings.extras_detail = request.POST.get('extras_detail', innings.extras_detail)
        innings.current_run_rate = float(request.POST.get('current_run_rate', innings.current_run_rate) or 0)
        innings.required_rate = float(request.POST.get('required_rate', innings.required_rate) or 0)
        innings.status_text = request.POST.get('status_text', innings.status_text)
        innings.result = request.POST.get('result', innings.result)
        innings.fall_of_wickets = request.POST.get('fall_of_wickets', innings.fall_of_wickets)
        
        # Match-level status
        match.status = request.POST.get('match_status', match.status)
        
        # Batting data (11 batters)
        batting = []
        for i in range(1, 12):
            batter = {
                'name': request.POST.get(f'bat_name_{i}', f'Batter {i}'),
                'runs': int(request.POST.get(f'bat_runs_{i}', 0) or 0),
                'balls': int(request.POST.get(f'bat_balls_{i}', 0) or 0),
                'fours': int(request.POST.get(f'bat_fours_{i}', 0) or 0),
                'sixes': int(request.POST.get(f'bat_sixes_{i}', 0) or 0),
                'how_out': request.POST.get(f'bat_howout_{i}', 'batting'),
                'at_crease': request.POST.get(f'bat_crease_{i}') == 'on',
            }
            batting.append(batter)
        innings.batting_data = batting
        
        # Bowling data (8 bowlers)
        bowling = []
        for i in range(1, 9):
            bowler = {
                'name': request.POST.get(f'bowl_name_{i}', f'Bowler {i}'),
                'overs': float(request.POST.get(f'bowl_overs_{i}', 0) or 0),
                'maidens': int(request.POST.get(f'bowl_maidens_{i}', 0) or 0),
                'runs': int(request.POST.get(f'bowl_runs_{i}', 0) or 0),
                'wickets': int(request.POST.get(f'bowl_wickets_{i}', 0) or 0),
                'is_active': request.POST.get(f'bowl_active_{i}') == 'on',
            }
            bowling.append(bowler)
        innings.bowling_data = bowling
        
        innings.save()
        
        # Update match-level score summary from innings
        inn1 = Innings.objects.filter(match=match, innings_number=1).first()
        inn2 = Innings.objects.filter(match=match, innings_number=2).first()
        if inn1:
            match.team1_score = f"{inn1.total_runs}/{inn1.wickets}"
            match.team1_overs = inn1.overs
        if inn2:
            match.team2_score = f"{inn2.total_runs}/{inn2.wickets}"
            match.team2_overs = inn2.overs
        
        # Update result text from whichever innings has it
        if innings.result:
            match.result_text = innings.result
        
        match.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Scorecard saved!'})
        return redirect(f'/dashboard/cricket/{match.id}/live/?innings={innings_num}')
    
    # Pad batting/bowling data to expected sizes if short
    batting_data = innings.batting_data or []
    while len(batting_data) < 11:
        batting_data.append({'name': f'Batter {len(batting_data)+1}', 'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 'how_out': 'batting', 'at_crease': False})
    
    bowling_data = innings.bowling_data or []
    while len(bowling_data) < 8:
        bowling_data.append({'name': f'Bowler {len(bowling_data)+1}', 'overs': 0, 'maidens': 0, 'runs': 0, 'wickets': 0, 'is_active': False})
    
    # Add 1-indexed position to each entry
    for idx, b in enumerate(batting_data):
        b['pos'] = idx + 1
    for idx, b in enumerate(bowling_data):
        b['pos'] = idx + 1
    
    context = {
        'match': match,
        'innings': innings,
        'innings_num': innings_num,
        'batting_data': batting_data,
        'bowling_data': bowling_data,
    }
    return render(request, 'dashboard/cricket_live.html', context)


@dashboard_login_required
def cricket_delete(request, match_id):
    """Delete a cricket match"""
    match = get_object_or_404(CricketMatch, id=match_id)
    match.is_active = False
    match.save()
    return redirect('cricket_list')


# ========== ICE CREAM ORDERS ==========

@dashboard_login_required
def orders_list(request):
    """List all ice cream orders"""
    status_filter = request.GET.get('status', '')
    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'dashboard/orders_list.html', {
        'orders': orders,
        'status_filter': status_filter,
    })


@csrf_exempt
@dashboard_login_required
def order_update_status(request, order_id):
    """Update order status via AJAX"""
    if request.method == 'POST':
        order = get_object_or_404(Order, order_id=order_id)
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'accept':
            order.status = 'confirmed'
            order.payment_status = 'verified'
        elif action == 'reject':
            order.status = 'cancelled'
            order.payment_status = 'failed'
        elif action == 'ship':
            order.status = 'shipped'
        elif action == 'deliver':
            order.status = 'delivered'
        
        order.save()
        return JsonResponse({'success': True, 'status': order.status})
    return JsonResponse({'success': False}, status=405)


# ========== NEWS MANAGEMENT ==========

@dashboard_login_required
def news_list(request):
    """List all news articles"""
    articles = News.objects.all()
    return render(request, 'dashboard/news_list.html', {'articles': articles})


@dashboard_login_required  
def news_add(request):
    """Add a news article"""
    if request.method == 'POST':
        from django.utils.text import slugify
        title = request.POST.get('title')
        News.objects.create(
            title=title,
            slug=slugify(title) + '-' + str(int(timezone.now().timestamp())),
            content=request.POST.get('content', ''),
            excerpt=request.POST.get('excerpt', ''),
            source=request.POST.get('source', ''),
            is_featured=request.POST.get('is_featured') == 'on',
            is_published=request.POST.get('is_published', 'on') == 'on',
            published_at=timezone.now(),
            image_url=request.POST.get('image_url', ''),
        )
        return redirect('dashboard_news')
    categories = NewsCategory.objects.all()
    return render(request, 'dashboard/news_form.html', {'action': 'Add', 'categories': categories})


@dashboard_login_required
def news_delete(request, news_id):
    """Delete a news article"""
    article = get_object_or_404(News, id=news_id)
    article.delete()
    return redirect('dashboard_news')


# ========== CRICKET PUBLIC API ==========

def cricket_api_matches(request):
    """Public API - returns active matches as JSON for the cricket score page"""
    matches = CricketMatch.objects.filter(is_active=True).order_by('-match_date')[:10]
    data = []
    for m in matches:
        # Get innings data
        innings_data = []
        for inn in m.innings_set2.all():
            innings_data.append({
                'number': inn.innings_number,
                'battingTeam': inn.batting_team,
                'score': inn.score_display,
                'overs': inn.overs,
                'statusText': inn.status_text,
                'result': inn.result,
            })
        
        data.append({
            'id': m.id,
            'series': m.series_name,
            'status': m.status,
            'team1': {'name': m.team1_name, 'abbr': m.team1_abbr, 'score': m.team1_score, 'overs': m.team1_overs},
            'team2': {'name': m.team2_name, 'abbr': m.team2_abbr, 'score': m.team2_score, 'overs': m.team2_overs},
            'result': m.result_text,
            'venue': m.venue,
            'matchDate': m.match_date.isoformat(),
            'oversLimit': m.overs_limit,
            'innings': innings_data,
            'updatedAt': m.updated_at.isoformat(),
        })
    return JsonResponse({'matches': data})


# ========== SERVICES / SECOND-HAND MARKETPLACE MODERATION ==========

@dashboard_login_required
def dashboard_services(request):
    """List all marketplace services & items for moderation"""
    from services.models import Service
    status_filter = request.GET.get('status', 'pending')
    type_filter = request.GET.get('type', '')
    services = Service.objects.all().order_by('-created_at')

    if status_filter == 'pending':
        services = services.filter(is_active=False)
    elif status_filter == 'active':
        services = services.filter(is_active=True)

    if type_filter == 'second_hand':
        services = services.filter(service_type='second_hand')

    return render(request, 'dashboard/services_list.html', {
        'services': services,
        'status_filter': status_filter,
        'type_filter': type_filter,
    })

@csrf_exempt
@dashboard_login_required
def dashboard_services_update_status(request, service_id):
    """Update service listing fields via AJAX"""
    from services.models import Service
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'approve':
            service.is_active = True
        elif action == 'disapprove':
            service.is_active = False
        elif action == 'toggle_featured':
            service.is_featured = not service.is_featured
        elif action == 'toggle_verified':
            service.is_verified = not service.is_verified
            
        service.save()
        return JsonResponse({
            'success': True,
            'is_active': service.is_active,
            'is_featured': service.is_featured,
            'is_verified': service.is_verified
        })
    return JsonResponse({'success': False}, status=405)

@dashboard_login_required
def dashboard_services_delete(request, service_id):
    """Delete a marketplace service listing"""
    from services.models import Service
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('dashboard_services')


# ========== MATRIMONY PROFILE MANAGEMENT ==========

@dashboard_login_required
def matrimony_dashboard_list(request):
    """List all matrimony profiles for admin moderation"""
    status_filter = request.GET.get('status', 'pending')
    profiles = MatrimonyProfile.objects.all().order_by('-created_at')
    
    if status_filter == 'pending':
        profiles = profiles.filter(is_approved=False, is_active=True)
    elif status_filter == 'approved':
        profiles = profiles.filter(is_approved=True, is_active=True)
    elif status_filter == 'inactive':
        profiles = profiles.filter(is_active=False)
    
    pending_count = MatrimonyProfile.objects.filter(is_approved=False, is_active=True).count()
    approved_count = MatrimonyProfile.objects.filter(is_approved=True, is_active=True).count()
    total_count = MatrimonyProfile.objects.filter(is_active=True).count()
    
    return render(request, 'dashboard/matrimony_list.html', {
        'profiles': profiles,
        'status_filter': status_filter,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'total_count': total_count,
    })


@dashboard_login_required
def matrimony_dashboard_add(request):
    """Admin can manually add a matrimony profile"""
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
            is_approved=True,
        )
        if request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
        profile.save()
        return redirect('matrimony_dashboard_list')
    
    castes = MatrimonyProfile.CASTE_CHOICES
    return render(request, 'dashboard/matrimony_form.html', {
        'action': 'Add',
        'castes': castes,
    })


@csrf_exempt
@dashboard_login_required
def matrimony_dashboard_update_status(request, profile_id):
    """Update matrimony profile status via AJAX"""
    if request.method == 'POST':
        profile = get_object_or_404(MatrimonyProfile, id=profile_id)
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'approve':
            profile.is_approved = True
        elif action == 'disapprove':
            profile.is_approved = False
        elif action == 'toggle_active':
            profile.is_active = not profile.is_active
        
        profile.save()
        return JsonResponse({
            'success': True,
            'is_approved': profile.is_approved,
            'is_active': profile.is_active,
        })
    return JsonResponse({'success': False}, status=405)


@dashboard_login_required
def matrimony_dashboard_delete(request, profile_id):
    """Delete a matrimony profile"""
    profile = get_object_or_404(MatrimonyProfile, id=profile_id)
    profile.delete()
    return redirect('matrimony_dashboard_list')
