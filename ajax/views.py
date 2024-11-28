from django.http import HttpResponse
from django.shortcuts import render

from dashboard.models import Games

def get_games(request):
    # if not post request then return empty response
    if not request.method == 'GET':
        return HttpResponse('')

    game_name = request.GET.get('search')
    if not game_name:
        games = Games.objects.all()[0:30]
    else:
        games = Games.objects.filter(name__icontains=game_name)[0:30]
    return render(request, 'ajax/get_games.html', {'games': games})
