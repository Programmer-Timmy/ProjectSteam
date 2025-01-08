from django.db.models import Sum, F, FloatField
from django.db.models.functions import ExtractWeek, Cast, Round

from dashboard.models import GameSessions


def get_total_played_data(year, user_id):
    """
    Get the total time played per game for a user in a specific year.
    """
    return list(
        GameSessions.objects.filter(user_game__user__id=user_id, start_timestamp__year=year)
        .values(game_name=F('user_game__app__name'), app_id=F('user_game__app__appid'))
        .annotate(total_time=Cast(Round(Sum('total_time'), 2), output_field=FloatField()))
    )


def get_weekly_played_data(year, start_week, end_week, user_id):
    """
    Get the weekly time played per game for a user within a week range in a specific year.
    """
    return list(
        GameSessions.objects.filter(
            user_game__user__id=user_id,
            start_timestamp__year=year,
            start_timestamp__week__gte=start_week,
            start_timestamp__week__lte=end_week
        )
        .annotate(week=ExtractWeek('start_timestamp'))
        .values(week=F('week'), game_name=F('user_game__app__name'), app_id=F('user_game__app__appid'))
        .annotate(total_time=Cast(Sum('total_time'), output_field=FloatField()))
        .order_by('week', 'game_name')
    )


def format_time(total_hours):
    """
    Format a duration in hours and minutes.
    """
    if total_hours:
        hours = int(total_hours)
        minutes = round((total_hours - hours) * 60)
        return f"{hours} hours and {minutes} minutes"
    return "0 hours and 0 minutes"
