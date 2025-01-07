from django.urls import path

from account import views

app_name = 'account'
urlpatterns = [
    path('', views.index, name='profile'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('settings/', views.settings, name='settings'),
    path('delete/', views.delete, name='delete'),
    path('game_library/', views.games, name='game_library'),
    path('game_library/<int:user_id>/', views.games, name='game_library'),

]
