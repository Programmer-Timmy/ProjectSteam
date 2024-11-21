from http.client import responses

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.models import Games, GameCategoriesLink


# Create your views here.

@login_required
def index(request):
    # get the top 10 avarage playtime of the games

    top_10_games = Games.objects.order_by('-average_playtime')[:10]

    games_with_categories = []
    for game in top_10_games:
        # Use select_related for optimized fetching of related category data
        categories = GameCategoriesLink.objects.filter(app_id=game).select_related('category')
        print(categories)
        category_names = [category.category.category_name for category in categories]

        games_with_categories.append({
            'game': game,
            'categories': category_names,
        })

    print(games_with_categories)

    return render(request, 'dashboard/index.html', {
        'page_title': 'Dashboard',
        'top_10_games': top_10_games,
        'games_with_categories': games_with_categories
    })
