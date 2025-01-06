from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from controlers.api.SteamApi import SteamApi
from controlers.api.SteamSpyApi import SteamSpyApi
from games.models import Games
from games.utils import update_game_with_steam_data, \
    get_sorted_unique_game_categories, get_sorted_unique_game_genres, get_sorted_unique_game_platforms, \
    get_sorted_unique_game_tags


def index(request):
    """
    Renders the homepage displaying games based on the search query and limit.

    Args:
        request (HttpRequest): The request object containing user inputs (search, limit).

    Returns:
        HttpResponse: The rendered 'games/index.html' template with game data.
    """
    limit = int(request.GET.get('limit', 30))
    search = request.GET.get('search', '')

    # Fetch games from the database with optional search filter
    if search:
        games = Games.objects.filter(name__icontains=search).order_by('appid')[:limit]
    else:
        games = Games.objects.all().order_by('appid')[:limit]

    return render(request, 'games/index.html', {
        'page_title': 'Games',
        'games': games,
        'search': search,
        'limit': limit
    })


def game(request, game_id):
    """
    Renders the game detail page for a specific game by appid, fetching data if necessary.

    Args:
        request (HttpRequest): The request object containing user inputs (limit, search).
        game_id (int): The appid of the game to display.

    Returns:
        HttpResponse: The rendered 'games/game.html' template with detailed game data.
    """
    limit = int(request.GET.get('limit', 30))
    search = request.GET.get('search', '')

    game = get_object_or_404(Games, appid=game_id)
    game.steam_url = f"https://store.steampowered.com/app/{game.appid}&l=en"

    if not all([game.steam_image, game.description, game.short_description, game.price,
                game.developer, game.publisher, game.release_date, game.positive_ratings,
                game.negative_ratings, game.owners]):
        print(f"Fetching data for {game.name}...")

        steam_data = SteamApi.fetch_steam_game_data(game.appid)
        steam_spy_data = SteamSpyApi.get_steam_game_data(game.appid)

        if steam_data and steam_spy_data:
            game = update_game_with_steam_data(game, steam_data, steam_spy_data)

    game.categories = get_sorted_unique_game_categories(game)
    game.genres = get_sorted_unique_game_genres(game)
    game.platforms = get_sorted_unique_game_platforms(game)
    game.steamspy_tags = get_sorted_unique_game_tags(game)

    return render(request, 'games/game.html', {
        'page_title': game.name,
        'game': game,
        'search': search,
        'limit': limit
    })
