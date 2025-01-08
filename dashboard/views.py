from django.contrib.auth.decorators import login_required
from django.db.models.functions import Round
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import F, Sum, Count, Prefetch, ExpressionWrapper, FloatField

from account.models import Friend
from dashboard.models import GameSessions, UserGames
from games.models import Games, GameCategoriesLink
from games.playable_games.utils import get_playable_games
from games.utils import get_available_years
from .utils import get_total_played_data, get_weekly_played_data, format_time


@login_required
def index(request):
    """
    Dashboard index view displaying user statistics, games, and friends.
    """
    top_10_games = (
        Games.objects.order_by('-average_playtime')
        .filter(average_playtime__isnull=False)[:10]
        .prefetch_related(
            Prefetch(
                'game_category_links',
                queryset=GameCategoriesLink.objects.select_related('category'),
                to_attr='fetched_categories'
            )
        )
    )

    best_reviewed_games = (
        Games.objects.annotate(
            average_rating=F('positive_ratings') / (F('negative_ratings') + 1)
        )
        .filter(average_rating__isnull=False)
        .order_by('-average_rating')[:10]
    )

    last_played = GameSessions.objects.filter(user_game__user=request.user).order_by('-start_timestamp')[:6]

    total_hours = UserGames.objects.filter(user=request.user).aggregate(
        total=ExpressionWrapper(Sum('hours_played') / 60.0 , output_field=FloatField())
    )['total']

    print(total_hours)

    total_playtime = format_time(total_hours)

    average_playtime = GameSessions.objects.filter(user_game__user=request.user).aggregate(
        average=Sum('total_time') / Count('id')
    )['average']
    average_playtime = format_time(average_playtime)

    friends = Friend.objects.filter(user=request.user, friend__opt_out=False)
    print(get_playable_games())
    return render(request, 'dashboard/index.html', {
        'page_title': 'Dashboard',
        'top_10_games': top_10_games,
        'best_reviewed_games': best_reviewed_games,
        'last_played_games': last_played,
        'total_playtime': total_playtime,
        'average_playtime': average_playtime,
        'friends': friends,
        'playable_games': get_playable_games()
    })


@login_required
def data(request):
    """
    Fetch and return user's game statistics as JSON.
    """
    year = request.GET.get('year')
    start_week = int(request.GET.get('startWeek'))
    end_week = int(request.GET.get('endWeek'))
    user_id = request.GET.get('userId', request.user.id)

    if not Friend.objects.filter(user=request.user, friend__id=user_id, friend__opt_out=False).exists() and user_id != request.user.id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if not year or not (1 <= start_week <= 53) or not (1 <= end_week <= 53):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    year = int(year)
    available_years = get_available_years(user_id)
    if year not in available_years and available_years:
        year = available_years[-1]

    total_played = get_total_played_data(year, user_id)
    weekly_played = get_weekly_played_data(year, start_week, end_week, user_id)

    return JsonResponse({
        'totalPlayed': total_played,
        'weeklyPlayed': weekly_played,
        'availableYears': available_years,
        'selectedYear': year
    })
