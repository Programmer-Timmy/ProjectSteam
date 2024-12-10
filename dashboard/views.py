from datetime import datetime, timedelta
from http.client import responses

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Prefetch, Sum, ExpressionWrapper, F
from django.db.models.functions import ExtractWeek
from django.forms import DurationField, FloatField
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models.functions import Cast

from dashboard.models import Games, GameCategoriesLink, UserGames, GameSessions


# Create your views here.

@login_required
def index(request):
    # get the top 10 avarage playtime of the games

    top_10_games = Games.objects.order_by('-average_playtime')[:10]
    from django.db.models import F, FloatField

    best_reviewed_games = (
        Games.objects.annotate(
            average_rating=F('positive_ratings') / (F('negative_ratings') + 1)  # Prevent division by zero
        )
        .order_by('-average_rating')[:10]  # Sort by highest average
    )

    # Prefetch related categories efficiently
    top_10_games = top_10_games.prefetch_related(
        Prefetch(
            'game_category_links',  # Matches the related_name in GameCategoriesLink
            queryset=GameCategoriesLink.objects.select_related('category'),
            to_attr='fetched_categories'
        )
    )

    # calulate total time played per game

    # get the total of all the games time and set it to a new field called total
    last_played = GameSessions.objects.filter(user_game__user=request.user
                                              ).order_by('-start_timestamp')[:6]

    return render(request, 'dashboard/index.html', {
        'page_title': 'Dashboard',
        'top_10_games': top_10_games,
        'best_reviewed_games': best_reviewed_games,
        'last_played_games': last_played,
    })

def get_total_played_data(year, user_id):
    total_played_per_game = (
        GameSessions.objects.filter(user_game__user__id=user_id, start_timestamp__year=year)
        .values(game_name=F('user_game__app__name'), app_id=F('user_game__app__appid'))
        .annotate(total_time=Cast(Sum('total_time'), output_field=models.FloatField()))
    )

    return list(total_played_per_game)


def get_weekly_played_data(year, start_week, end_week, user_id):
    played_per_game_per_week = (
        GameSessions.objects.filter(
            user_game__user__id=user_id,
            start_timestamp__year=year,
            start_timestamp__week__gte=start_week,
            start_timestamp__week__lte=end_week
        )
        .annotate(week=ExtractWeek('start_timestamp'))
        .values(week=F('week'), game_name=F('user_game__app__name'), app_id=F('user_game__app__appid'))
        .annotate(total_time=Cast(Sum('total_time'), output_field=models.FloatField()))
        .order_by('week', 'game_name')
    )

    return list(played_per_game_per_week)

def data(request):
    year = request.GET.get('year')
    start_week = int(request.GET.get('startWeek'))
    end_week = int(request.GET.get('endWeek'))

    if not year or not (1 <= start_week <= 53) or not (1 <= end_week <= 53):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    # Generate date range for the selected year and week range
    year = int(year)

    # Query your database to get data for the selected week range
    total_played = get_total_played_data(year, request.user.id)
    weekly_played = get_weekly_played_data(year, start_week, end_week, request.user.id)

    return JsonResponse({
        'totalPlayed': total_played,
        'weeklyPlayed': weekly_played,
    })

