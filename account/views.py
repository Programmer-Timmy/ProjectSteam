import os

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import ExpressionWrapper, F, FloatField
from django.db.models.functions import Round
from django.http import JsonResponse
from django.shortcuts import render, redirect

from AuthManager.models import CustomUser
from account.forms import ProfileEditForm, UserSettingsForm, UserChangePasswordForm
from account.models import Friend
from dashboard.models import GameSessions, UserGames


@login_required
def index(request):
    """
    Index view for the account app.

    Displays the user's profile page, including:
    - Last 3 games played.
    - Friends with public profiles.
    - Profile image status and path.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered profile page.
    """
    last_played_games = GameSessions.objects.filter(user_game__user=request.user).order_by('-start_timestamp')[:3]
    friends = Friend.objects.filter(user=request.user, friend__public_profile=True)
    steam_friends = Friend.objects.filter(user=request.user, steam_id__isnull=False)

    img_exists = False
    image_path = os.path.join('media', 'profile_images', f'{request.user.id}.jpg')

    user_games = UserGames.objects.filter(user=request.user).order_by('?')[:6]
    for user_game in user_games:
        user_game.hours_played = round(user_game.hours_played / 60, 1)

    if os.path.exists(image_path):
        img_exists = True

    return render(request, 'account/index.html', {
        'page_title': 'Profile',
        'last_played_games': last_played_games,
        'friends': friends,
        'img_exists': img_exists,
        'steam_friends': steam_friends,
        'user_games': user_games,
    })


@login_required
def profile(request, user_id):
    """
    Profile view for the account app.

    Displays the profile of the specified user if the profile is public.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user whose profile is being viewed.

    Returns:
        HttpResponse: Rendered profile page or 404 page if the profile is private or nonexistent.
    """
    if user_id == request.user.id:
        return redirect('account:profile')

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return render(request, '404.html', {
            'page_title': '404',
        })

    if not user.public_profile or user.opt_out:
        return render(request, '404.html', {
            'page_title': '404',
        })

    friends = Friend.objects.filter(user=user, friend__public_profile=True, friend__opt_out=False)
    steam_friends = Friend.objects.filter(user=user, steam_id__isnull=False)
    last_played_games = GameSessions.objects.filter(user_game__user=user).order_by('-start_timestamp')[:3]
    user_games = UserGames.objects.filter(user=user).order_by('?')[:6]
    for user_game in user_games:
        user_game.hours_played = round(user_game.hours_played / 60, 1)

    return render(request, 'account/profile.html', {
        'page_title': f"{user.username}'s Profile",
        'last_played_games': last_played_games,
        'friends': friends,
        'user_profile': user,
        'steam_friends': steam_friends,
        'user_games': user_games,
    })


@login_required
def edit(request):
    """
    Edit view for the account app.

    Allows the user to edit their profile details.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered edit page or redirect to profile on successful save.
    """
    form = ProfileEditForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')

    return render(request, 'account/edit.html', {
        'page_title': 'Edit Account',
        'form': form,
    })


@login_required
def settings(request):
    """
    Settings view for the account app.

    Allows the user to edit their account settings, including changing their password.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered settings page.
    """
    success_message = False
    if request.method == 'POST':
        if 'password' in request.POST:
            password_form = UserChangePasswordForm(request.POST, instance=request.user)
            form = UserSettingsForm(instance=request.user)
            if password_form.is_valid():
                password_form.save()
                success_message = 'Password updated successfully.'
        else:
            form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
            password_form = UserChangePasswordForm(instance=request.user)
            if form.is_valid():
                form.save()
                success_message = 'Settings updated successfully.'
    else:
        form = UserSettingsForm(instance=request.user)
        password_form = UserChangePasswordForm(instance=request.user)

    return render(request, 'account/settings.html', {
        'page_title': 'Settings',
        'form': form,
        'password_form': password_form,
        'success_message': success_message,
    })


@login_required
def delete(request):
    """
    Delete view for the account app.

    Allows the user to delete their account.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered delete page or redirect to index on successful deletion.
    """
    success_message = False
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        success_message = 'Account deleted successfully.'

    return render(request, 'account/delete.html', {
        'page_title': 'Delete Account',
        'success_message': success_message,
    })

@login_required
def games(request, user_id = None):
    if user_id is None:
        user_id = request.user.id

    user = CustomUser.objects.get(pk=user_id)
    userGames = UserGames.objects.filter(user_id=user_id) \
        .annotate(hours_played_annotation=Round(ExpressionWrapper(F('hours_played') / 60.0, output_field=FloatField()), 1)) \
        .order_by('-hours_played_annotation')

    if user.opt_out or not user.public_profile or not user.steam_id:
        return render(request, '404.html', {
            'page_title': '404',
        })

    return render(request, 'account/games.html', {
        'page_title': 'Game Library - ' + user.username,
        'user': user,
        'userGames': userGames,
        'request_user': request.user,
    })

