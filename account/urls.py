from django.urls import path

from account import views

app_name = 'account'
urlpatterns = [
    path('', views.index, name='profile'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
]
