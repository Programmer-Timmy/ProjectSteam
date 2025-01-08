from django.urls import path

from . import views

app_name = 'satisfactory_api'

urlpatterns = [
    path("", views.satisfactory_api, name="index"),
    path("delete/<int:id>/", views.delete_satisfactory_api, name="satisfactory_api_delete"),
    path("download/<int:id>/<str:save_name>/", views.download_satisfactory_api, name="satisfactory_api_download"),
    path("updateSettings/<int:id>/", views.update_satisfactory_api, name="update_satisfactory_api"),
    path("updateAdvancedGameSettings/<int:id>/", views.update_advanced_game_settings, name="update_advanced_game_settings"),
    path("shutdownServer/<int:id>/", views.shutdown_server, name="shutdown_server"),
    path("<int:id>/", views.satisfactory_api_details, name="satisfactory_api_details"),
    path("getServerInfo/<int:id>/", views.get_server_info, name="get_server_info"),
]