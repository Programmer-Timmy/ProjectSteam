from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('need_accout/', views.need_account, name='need_account'),
    path('connect_steam/', views.connect_steam, name='connect_steam'),
]
