from django.urls import path

from . import views

app_name = 'hangman'

urlpatterns = [
    path("", views.hangman, name="index"),
]