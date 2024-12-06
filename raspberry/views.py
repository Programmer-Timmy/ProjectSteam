from django.shortcuts import render, get_object_or_404

# Create your views here.
import requests
from django.http import JsonResponse
from AuthManager.models import CustomUser


def get_online_status_from_User(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    online_status = user.is_online

    return render(request, 'raspberry/online_status.html', {'user': user, 'is_online': online_status})
