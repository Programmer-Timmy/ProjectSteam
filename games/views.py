from django.shortcuts import render

from dashboard.models import Games


# Create your views here.
def index(request):
    # get all games from the database
    games = Games.objects.all()[0:30]

    return render(request, 'games/index.html', {
        'page_title': 'Games',
        'games': games
   })


def game(request, game_id):
    # get the game from the database
    print(game_id)
    game = Games.objects.get(appid=game_id)

    game.categories = [link.category.category_name for link in game.game_category_links.all()]
    game.categories = list(set(game.categories))
    game.categories.sort()

    return render(request, 'games/game.html', {
        'page_title': game.name,
        'game': game
    })
# Compare this snippet from games/views.py:



