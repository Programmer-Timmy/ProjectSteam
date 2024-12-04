from http.client import responses

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render

from dashboard.models import Games, GameCategoriesLink, UserGames


# Create your views here.

@login_required
def index(request):
    # get the top 10 avarage playtime of the games

    top_10_games = Games.objects.order_by('-average_playtime')[:10]
    from django.db.models import F, FloatField

    best_reviewed_games = (
        Games.objects.annotate(
            average_rating=F('positive_ratings') / (F('negative_ratings') + 1)  # Prevent division by zero
        )
        .order_by('-average_rating')[:10]  # Sort by highest average
    )

    # Prefetch related categories efficiently
    top_10_games = top_10_games.prefetch_related(
        Prefetch(
            'game_category_links',  # Matches the related_name in GameCategoriesLink
            queryset=GameCategoriesLink.objects.select_related('category'),
            to_attr='fetched_categories'
        )
    )

    last_played = UserGames.objects.filter(user=request.user).order_by('-last_played')[:10]
    print(last_played)

    return render(request, 'dashboard/index.html', {
        'page_title': 'Dashboard',
        'top_10_games': top_10_games,
        'best_reviewed_games': best_reviewed_games,
        'last_played_games': last_played
    })
