from datetime import datetime, timedelta
from http.client import responses

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Prefetch, Sum, ExpressionWrapper, F, Count
from django.db.models.functions import ExtractWeek
from django.forms import DurationField, FloatField
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models.functions import Cast

from account.models import Friend
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

    total_hours = GameSessions.objects.filter(user_game__user=request.user).aggregate(total=Sum('total_time'))['total']

    if total_hours:

        hours = int(total_hours)  # Get the whole hours part
        minutes = round((total_hours - hours) * 60)

        total_playtime = f"{hours} hours and {minutes} minutes"
    else:
        total_playtime = "0 hours and 0 minutes"

    # get the average playtime of all the games

    average_playtime  = GameSessions.objects.filter(
        user_game__user=request.user
    ).aggregate(
        average=Sum('total_time') / Count('id')
    )['average']

    if average_playtime:
        average_hours = int(average_playtime)
        average_minutes = round((average_playtime - average_hours) * 60)
        average_playtime = f"{average_hours} hours and {average_minutes} minutes"
    else:
        average_playtime = "0 hours and 0 minutes"



    friends = Friend.objects.filter(user=request.user, friend__opt_out=False)
    return render(request, 'dashboard/index.html', {
        'page_title': 'Dashboard',
        'top_10_games': top_10_games,
        'best_reviewed_games': best_reviewed_games,
        'last_played_games': last_played,
        'total_playtime': total_playtime,
        'average_playtime': average_playtime,
        'friends': friends,
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
    user_id = request.GET.get('userId', request.user.id)
    print(user_id)

    # check if user is friends and not oped out
    if not Friend.objects.filter(user=request.user, friend__id=user_id, friend__opt_out=False).exists() and user_id != request.user.id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if not year or not (1 <= start_week <= 53) or not (1 <= end_week <= 53):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    # Generate date range for the selected year and week range
    year = int(year)

    # Query your database to get data for the selected week range
    total_played = get_total_played_data(year, user_id)
    weekly_played = get_weekly_played_data(year, start_week, end_week, user_id)

    return JsonResponse({
        'totalPlayed': total_played,
        'weeklyPlayed': weekly_played,
    })

