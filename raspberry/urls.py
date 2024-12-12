from django.urls import path
from raspberry import views
from raspberry.views import set_online_status

app_name = 'raspberry'

urlpatterns = [
    # path('<int:user_id>/status/', views.get_online_status_from_User, name='is_online'),
    path('get_status/', views.get_online_status_from_user, name='is_online'),

    path('status/', set_online_status, name='status'),


]
