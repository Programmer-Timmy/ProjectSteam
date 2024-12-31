import json
from datetime import datetime

import requests
from django.shortcuts import render, get_object_or_404

from dashboard.models import Games, GamePlatforms, GameGenres, GameCategories, GameSteamspyTags


# Create your views here.
def index(request):
    # get all games from the database
    games = Games.objects.all().order_by('appid')[0:30]

    return render(request, 'games/index.html', {
        'page_title': 'Games',
        'games': games
    })

def fetch_steam_data(appid):
    """
    Fetch game data from Steam Store API based on the game's name.
    """

    try:
        app_url = f"https://store.steampowered.com/api/appdetails/?appids={appid}&l=en"
        response = requests.get(app_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            try:
                return data[str(appid)]['data']
            except KeyError:
                return None

        return None
    except (requests.RequestException, ValueError):
        return None

def fetch_steam_spy_data(appid):
    """
    Fetch game data from Steam Spy API based on the game's name.
    """

    try:
        app_url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
        response = requests.get(app_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            return data

        return None
    except (requests.RequestException, ValueError):
        return None

def game(request, game_id):
    # Get the game from the database
    game = get_object_or_404(Games, appid=game_id)

    game.steam_url = f"https://store.steampowered.com/app/{game.appid}&l=en"

    # cache the game's image, description, and short description because of the API rate limit
    if not game.steam_image or not game.description or not game.short_description or not game.price or not game.developer or not game.publisher or not game.release_date or not game.achievements or not game.positive_ratings or not game.negative_ratings or not game.owners or not game.median_playtime or not game.average_playtime or not game.required_age:
        # Fetch Steam API data using the game's name
        steam_data = fetch_steam_data(game.appid)
        steam_spy_data = fetch_steam_spy_data(game.appid)
        if steam_data:
            platforms = steam_data.get('platforms', {})
            release_date = steam_data.get('release_date', {}).get('date', '')
            # needs to go to  YYYY-MM-DD
            date_obj = datetime.strptime(release_date, '%d %b, %Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')

            game.release_date = formatted_date
            game.steam_image = steam_data['header_image']
            game.description = steam_data.get('detailed_description', '')
            game.short_description = steam_data.get('short_description', '')
            game.price = steam_data.get('price_overview', {}).get('final', 0) / 100
            game.developer = steam_data.get('developers', [''])[0]
            game.publisher = steam_data.get('publishers', [''])[0]
            game.achievements = steam_data.get('achievements', {}).get('total', 0)
            game.positive_ratings = steam_spy_data.get('positive', 0)
            game.negative_ratings = steam_spy_data.get('negative', 0)
            game.owners = steam_spy_data.get('owners', '')
            game.median_playtime = steam_spy_data.get('median_playtime', 0)
            game.average_playtime = steam_spy_data.get('average_playtime', 0)
            game.required_age = steam_data.get('', 0)

            for platform in steam_data.get('platforms', {}).keys():
                if platforms[platform] is True:
                    GamePlatforms.objects.get_or_create(platform_name=platform)
                    game_platform = GamePlatforms.objects.get(platform_name=platform)
                    game.game_platform_links.get_or_create(platform=game_platform)

            for genre in steam_data.get('genres', []):

                GameGenres.objects.get_or_create(genre_name=genre['description'])
                game_genre = GameGenres.objects.get(genre_name=genre['description'])
                game.game_genre_links.get_or_create(genre=game_genre)

            for category in steam_data.get('categories', []):
                GameCategories.objects.get_or_create(category_name=category['description'])
                GameSteamspyTags.objects.get_or_create(tag_name=category['description'])
                game_category = GameCategories.objects.get(category_name=category['description'])
                game_tag = GameSteamspyTags.objects.get(tag_name=category['description'])
                game.game_category_links.get_or_create(category=game_category)
                game.game_tag_links.get_or_create(tag=game_tag)

            # Update the game with the new data
            game.save()

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
