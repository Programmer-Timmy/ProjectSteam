from django.shortcuts import render, redirect

from AuthManager.models import CustomUser
from account.forms import ProfileEditForm
from account.models import Friend
from dashboard.models import UserGames


# Create your views here.

def index(request):
    last_played_games = UserGames.objects.filter(user=request.user).order_by('-last_played')[:3]
    friends = Friend.objects.filter(user=request.user, friend__public_profile=True)
    return render(request, 'account/index.html', {
        'page_title': 'Profile',
        'last_played_games': last_played_games,
        'friends': friends,
    })

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
    if not user.public_profile:
        return render(request, '404.html', {
            'page_title': '404',
        })

    friends = Friend.objects.filter(user=user, friend__public_profile=True)
    last_played_games = UserGames.objects.filter(user=user).order_by('-last_played')[:3]

    return render(request, 'account/profile.html', {
        'page_title': f'{user.username}\'s Profile',
        'last_played_games': last_played_games,
        'friends': friends,
        'user': user,
    })

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
