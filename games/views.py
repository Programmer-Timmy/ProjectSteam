import json

import requests
from django.shortcuts import render, get_object_or_404

from dashboard.models import Games


# Create your views here.
def index(request):
    # get all games from the database
    games = Games.objects.all()[0:30]

    return render(request, 'games/index.html', {
        'page_title': 'Games',
        'games': games
    })


def fetch_steam_data(appid):
    """
    Fetch game data from Steam Store API based on the game's name.
    """

    try:
        app_url = f"https://store.steampowered.com/api/appdetails/?appids={appid}"
        response = requests.get(app_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            return data[str(appid)]['data']

        return None
    except (requests.RequestException, ValueError):
        return None


def game(request, game_id):
    # Get the game from the database
    game = get_object_or_404(Games, appid=game_id)

    # Fetch Steam API data using the game's name

    steam_data = fetch_steam_data(game.appid)
    # nice print
    print(json.dumps(steam_data, indent=4))
    if steam_data:
        game.steam_image = steam_data.get('header_image', steam_data.get('tiny_image'))  # Game image
        game.steam_url = f"https://store.steampowered.com/app/{game.appid}"
        game.description = steam_data.get('detailed_description')  # Game description
        game.short_description = steam_data.get('short_description')  # Game short description
    else:
        game.steam_image = None
        game.steam_url = None

    print(game.steam_image)
    print(game.steam_url)

    # Organize categories
    game.categories = [link.category.category_name for link in game.game_category_links.all()]
    game.categories = list(set(game.categories))
    game.categories.sort()

    # Organize genres
    game.genres = [link.genre.genre_name for link in game.game_genre_links.all()]
    game.genres = list(set(game.genres))
    game.genres.sort()

    # Organize platforms
    game.platforms = [link.platform.platform_name for link in game.game_platform_links.all()]
    game.platforms = list(set(game.platforms))
    game.platforms.sort()

    # Organize tags
    game.steamspy_tags = [link.tag.tag_name for link in game.game_tag_links.all()]
    game.steamspy_tags = list(set(game.steamspy_tags))
    game.steamspy_tags.sort()

    return render(request, 'games/game.html', {
        'page_title': game.name,
        'game': game
    })
# Compare this snippet from games/views.py:
