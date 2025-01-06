import os

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from AuthManager.models import CustomUser
from account.forms import ProfileEditForm, UserSettingsForm, UserChangePasswordForm
from account.models import Friend
from dashboard.models import GameSessions


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
    print(last_played_games)
    friends = Friend.objects.filter(user=request.user, friend__public_profile=True)

    img_exists = False
    image_path = os.path.join('media', 'profile_images', f'{request.user.id}.jpg')

    if os.path.exists(image_path):
        img_exists = True

    return render(request, 'account/index.html', {
        'page_title': 'Profile',
        'last_played_games': last_played_games,
        'friends': friends,
        'img_exists': img_exists,
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
    last_played_games = GameSessions.objects.filter(user_game__user=user).order_by('-start_timestamp')[:3]

    return render(request, 'account/profile.html', {
        'page_title': f"{user.username}'s Profile",
        'last_played_games': last_played_games,
        'friends': friends,
        'user_profile': user,
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
