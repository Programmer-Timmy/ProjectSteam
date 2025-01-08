from tkinter import image_names

from django.urls import path, include

from . import views

app_name = 'playable_games'

urlpatterns = [
    path("", views.index, name="games-index"),
    path("satisfactory_api/", include('games.playable_games.satisfactory_api.urls'), name="satisfactory_api"),
    path("hangman/", include('games.playable_games.hangman.urls'), name="hangman"),
    path("flapy_bird/", include('games.playable_games.flapy_bird.urls'), name="flapy_bird"),

]