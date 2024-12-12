from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from AuthManager.models import CustomUser
from django.contrib import messages



# def get_online_status_from_User(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     online_status = user.is_online
#     return render(request, 'raspberry/online_status.html', {'user': user, 'is_online': online_status})

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

# @login_required
# def set_online_status(request):
#     if request.method == 'POST':
#         status = request.POST.get('status')  # Ophaal de status parameter uit de form data
#         is_online = status.lower() == 'true'  # Converteer naar bool op basis van de stringwaarde
#
#         if request.user.is_authenticated:
#             user = request.user
#             user.is_online = is_online
#             user.save()
#     return render(request, 'raspberry/set_status.html')


@csrf_exempt  # Disable CSRF for simplicity (not recommended for production)
def set_online_status(request):
    if request.method == "POST":
        api_key = request.POST.get('api_key')
        is_online = request.POST.get('is_online') == 'True'  # Convert string to boolean
        user = get_object_or_404(CustomUser, api_key=api_key)
        user.is_online = is_online
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=400)

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
#
# def set_online_status(request):
#     if request.method == "POST":
#         api_key = request.POST.get('api_key')
#         is_online = request.POST.get('is_online') == 'True'
#         user = get_object_or_404(CustomUser, api_key=api_key)
#         user.is_online = is_online
#         user.save()
#
#         # Send WebSocket notification
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "online_status",  # Group name
#             {
#                 "type": "status_update",
#                 "title": "Status Update",
#                 "message": f"User {user.username}'s online status updated to {'Online' if is_online else 'Offline'}.",
#             },
#         )
#
#         return JsonResponse({'success': True})
#     return JsonResponse({'error': 'Invalid method'}, status=400)