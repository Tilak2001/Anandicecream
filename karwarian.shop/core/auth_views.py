from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse


def _get_next_url(request):
    return request.GET.get('next') or request.POST.get('next') or reverse('matrimony_list')


def user_login(request):
    """Public user sign-in for matrimony and member features."""
    next_url = _get_next_url(request)
    if request.user.is_authenticated:
        return redirect(next_url)

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signed in successfully. You can now view matrimony profiles.')
            return redirect(next_url)
        error = 'Invalid username or password. Please try again.'

    return render(request, 'core/user_login.html', {
        'error': error,
        'next': next_url,
    })


def user_register(request):
    """Create a new site user account."""
    next_url = _get_next_url(request)
    if request.user.is_authenticated:
        return redirect(next_url)

    errors = []
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1:
            errors.append('Please fill in all required fields.')
        elif len(password1) < 6:
            errors.append('Password must be at least 6 characters.')
        elif password1 != password2:
            errors.append('Passwords do not match.')
        elif User.objects.filter(username__iexact=username).exists():
            errors.append('This username is already taken.')
        elif User.objects.filter(email__iexact=email).exists():
            errors.append('This email is already registered.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )
            login(request, user)
            messages.success(request, 'Account created! You are now signed in.')
            return redirect(next_url)

    return render(request, 'core/user_register.html', {
        'errors': errors,
        'next': next_url,
    })


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('home')
