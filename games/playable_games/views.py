import importlib
import os

from django.shortcuts import render, redirect
from dotenv import load_dotenv

load_dotenv()
hash_key = os.getenv('HASH_KEY')
hash_salt = os.getenv('HASH_SALT')

def index(request):
    """
    Renders the playable games page displaying games that are free to play.

    Args:
        request (HttpRequest): The request object containing user inputs (limit, search).

    Returns:
        HttpResponse: The rendered 'games/playable_games.html' template with free-to-play games.
    """
    IMAGES = {
        'satisfactory_api': 'https://portfolio.timmygamer.nl/img/66fe973b40b0f7.53385927.jpg',
    }

    DESCRIPTIONS = {
        'satisfactory_api': 'YES',
    }

    module = importlib.import_module('games.playable_games.urls')
    urlpatterns = getattr(module, 'urlpatterns').copy()

    urlpatterns.pop(0)  # Remove the index path
    games = []

    for url in urlpatterns:
        link = url.pattern._route.replace('/\Z', '').replace('^', '').replace('/', '')
        name = link.replace('_', ' ').title()
        games.append({
            'name': name,
            'url': "playable_games:" + link + ":index",
            'image_url': IMAGES.get(link, ''),
            'description': DESCRIPTIONS.get(link, ''),
        })


    return render(request, 'playable_games/playable_games.html', {
        'page_title': 'Playable Games',
        'games': games
    })