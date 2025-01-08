from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from social_django.models import UserSocialAuth

from .forms import CustomUserCreationForm, CustomLoginForm
from .models import CustomUser


def login_view(request):
    """
    Handle user login.

    If the request method is POST, validate the login form and authenticate the user.
    Redirect the user to the dashboard upon successful login, otherwise display errors.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered login page or redirect to the dashboard on success.
    """
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard-index')  # Redirect to the dashboard
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'AuthManager/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout.

    Log the user out and redirect to the index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirect to the index page.
    """
    logout(request)
    return redirect('index')


def register_view(request):
    """
    Handle user registration.

    If the request method is POST, validate the registration form and create a new user.
    Redirect the user to the login page upon successful registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered registration page or redirect to login on success.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page
    else:
        form = CustomUserCreationForm()

    return render(request, 'AuthManager/register.html', {'form': form})


def need_account(request):
    """
    Render the 'Need Account' page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'Need Account' page.
    """
    return render(request, 'AuthManager/need_account.html', {'page_title': 'Need Account', 'show_footer': False})


def connect_steam(request):
    """
    Handle Steam connection opt-out.

    If the request method is POST, update the user's Steam opt-out status.
    Redirect the user to the dashboard after saving.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered Steam connection page or redirect to dashboard.
    """
    if request.method == 'POST':
        user = request.user
        user.steam_opt_out = True
        user.save()
        return redirect('dashboard-index')

    return render(request, 'AuthManager/connect_steam.html', {'page_title': 'Connect Steam', 'show_footer': False})

def connected_steam(request):
    """
    Render the 'Connected Steam' page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'Connected Steam' page.
    """
    return render(request, 'AuthManager/steam_connected.html', {'page_title': 'Connected Steam', 'show_footer': False})


def disconnect_steam(request):
    """
    Handle Steam disconnection.

    If the request method is POST, remove the user's Steam social authentication
    association and clear related user data. Redirect the user to the dashboard.

    Args
    -------
    request : HttpRequest
        The HTTP request object.

    Returns
    -------
    HttpResponse
        Rendered Steam disconnection page or redirect to the dashboard.
    -------
    """
    if request.method == 'POST':
        user = request.user

        # Remove the Steam social authentication entry
        try:
            steam_auth = user.social_auth.get(provider='steam')
            steam_auth.delete()
        except UserSocialAuth.DoesNotExist:
            pass  # If no Steam connection exists, no action needed.

        # Clear additional user-related Steam details (optional)
        user.steam_id = ''
        user.avatar_url = ''
        user.steam_username = ''
        if user.use_steam_profile:
            user.username = user.original_username

        user.use_steam_profile = False
        user.save()

        return render(request, 'AuthManager/steam_disconnected.html', {'page_title': 'Disconnected Steam', 'show_footer': False})

    return render(request, 'AuthManager/disconnect_steam.html', {
        'page_title': 'Disconnect Steam',
        'show_footer': False
    })
