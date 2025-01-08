from django.urls import path

from . import views

app_name = 'flapy_bird'

urlpatterns = [
    path("", views.hangman, name="index"),
]