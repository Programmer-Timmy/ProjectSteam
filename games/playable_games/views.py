import os

from django.shortcuts import render
from dotenv import load_dotenv

from games.playable_games.utils import get_playable_games

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
    return render(request, 'playable_games/playable_games.html', {
        'page_title': 'Playable Games',
        'games': get_playable_games()
    })
