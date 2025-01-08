from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="games-index"),
    path("<int:game_id>/", views.game, name="game"),
    path("playable/" , include('games.playable_games.urls')),
]