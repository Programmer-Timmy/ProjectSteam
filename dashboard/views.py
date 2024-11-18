from http.client import responses

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.models import Games


# Create your views here.

@login_required
def index(request):
    # get the top 10 avarage playtime of the games

    top_10_games = Games.objects.order_by('-average_playtime')[:10]

    return render(request, 'dashboard/index.html', {'page_title': 'Dashboard', 'top_10_games': top_10_games})
