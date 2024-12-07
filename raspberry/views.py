from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from AuthManager.models import CustomUser



def get_online_status_from_User(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    online_status = user.is_online
    return render(request, 'raspberry/online_status.html', {'user': user, 'is_online': online_status})

@login_required
def set_online_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')  # Ophaal de status parameter uit de form data
        is_online = status.lower() == 'true'  # Converteer naar bool op basis van de stringwaarde

        if request.user.is_authenticated:
            user = request.user
            user.is_online = is_online
            user.save()
    return render(request, 'raspberry/set_status.html')


