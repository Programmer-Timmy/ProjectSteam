from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from dashboard.models import Games

def get_games(request):
    # if not post request then return empty response
    if not request.method == 'GET':
        return HttpResponse('')

    game_name = request.GET.get('search', None)
    order_by = request.GET.get('order_by', 'id')  # Default order_by column
    order_dir = request.GET.get('order', 'asc')  # Default order direction
    limit = request.GET.get('limit', '30')  # Default limit
    try:
        # Ensure limit is an integer
        limit = int(limit)
    except ValueError:
        return JsonResponse({'error': 'Invalid limit value'}, status=400)

    # Validate order direction
    if order_dir not in ['asc', 'desc']:
        return JsonResponse({'error': 'Invalid order direction'}, status=400)

        # Dynamically build the query
    query = Q()  # Start with an empty query
    if game_name:
        query &= Q(name__icontains=game_name)  # Add search filter if provided

    # Determine ordering
    order_prefix = '' if order_dir == 'asc' else '-'
    ordering = f'{order_prefix}{order_by}'

    # Execute the query
    games = Games.objects.filter(query).order_by(ordering)[:limit]

    return render(request, 'ajax/get_games.html', {'games': games})

# Render the response
