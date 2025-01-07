from channels.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from AuthManager.models import CustomUser



@login_required()
def get_is_to_close_status(request):
    user = request.user
    sitting_to_close = user.is_to_close
    response_data = {
        'username': user.username,
        'is_to_close': sitting_to_close
    }
    return JsonResponse(response_data)

@csrf_exempt
def set_is_to_close_status(request):
    if request.method == "POST":
        api_key = request.POST.get('api_key')
        is_to_close = request.POST.get('is_to_close') == 'True'
        user = get_object_or_404(CustomUser, api_key=api_key)
        user.is_to_close = is_to_close
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=400)


@login_required()
def get_online_status_from_user(request):
    user = request.user
    online_status = user.is_online
    response_data = {
        'user_id': user.id,
        'username': user.username,
        'is_online': online_status,
    }

    return JsonResponse(response_data)

@csrf_exempt
def set_online_status(request):
    if request.method == "POST":
        api_key = request.POST.get('api_key')
        is_online = request.POST.get('is_online') == 'True'  # Convert string to boolean
        user = get_object_or_404(CustomUser, api_key=api_key)
        user.is_online = is_online
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=400)
