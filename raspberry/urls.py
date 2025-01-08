from django.urls import path
from pyexpat import native_encoding

from raspberry import views

app_name = 'raspberry'

urlpatterns = [
    # path('<int:user_id>/status/', views.get_online_status_from_User, name='is_online'),
    path('get_status/', views.get_online_status_from_user, name='is_online'),
    path('status/', views.set_online_status, name='status'),
    path('is_to_close/', views.set_is_to_close_status, name='distance'),
    path('get_is_to_close/', views.get_is_to_close_status, name='is_to_close')

]
