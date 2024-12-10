from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from AuthManager.models import CustomUser
from account.forms import ProfileEditForm, UserSettingsForm, UserChangePasswordForm
from account.models import Friend
from dashboard.models import UserGames, GameSessions


# Create your views here.
@login_required
def index(request):
    last_played_games = GameSessions.objects.filter(user_game__user=request.user).order_by('-start_timestamp')[:3]
    friends = Friend.objects.filter(user=request.user, friend__public_profile=True)
    return render(request, 'account/index.html', {
        'page_title': 'Profile',
        'last_played_games': last_played_games,
        'friends': friends,
    })

@login_required
def profile(request, user_id):
    # if user id is the same as the logged in user
    if user_id == request.user.id:
        return redirect('account:profile')

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return render(request, '404.html', {
            'page_title': '404',
        })

    # if user is not public show default 404
    if not user.public_profile or user.opt_out:
        return render(request, '404.html', {
            'page_title': '404',
        })

    friends = Friend.objects.filter(user=user, friend__public_profile=True, friend__opt_out=False)
    last_played_games = GameSessions.objects.filter(user_game__user=user).order_by('-start_timestamp')[:3]

    return render(request, 'account/profile.html', {
        'page_title': f'{user.username}\'s Profile',
        'last_played_games': last_played_games,
        'friends': friends,
        'user_profile': user,
    })

@login_required
def edit(request):
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

    else :
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
    success_message = False
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        success_message = 'Account deleted successfully.'

    return render(request, 'account/delete.html', {
        'page_title': 'Delete Account',
        'success_message': success_message,
    })