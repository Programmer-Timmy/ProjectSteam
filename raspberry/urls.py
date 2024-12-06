from django.urls import path
from raspberry import views

app_name = 'raspberry'

urlpatterns = [
    path('<int:user_id>/status/', views.get_online_status_from_User, name='is_online'),
]
