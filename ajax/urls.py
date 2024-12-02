from django.urls import path

from . import views

urlpatterns = [
    path('get_games/', views.get_games, name='get_games'),
    path('dark_mode/', views.dark_mode, name='dark_mode'),
]
