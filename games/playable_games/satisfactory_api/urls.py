from django.urls import path

from . import views

app_name = 'satisfactory_api'

urlpatterns = [
    path("", views.satisfactory_api, name="index"),
    path("delete/<int:id>/", views.delete_satisfactory_api, name="satisfactory_api_delete"),
    path("download/<int:id>/<str:save_name>/", views.download_satisfactory_api, name="satisfactory_api_download"),
    path("<int:id>/", views.satisfactory_api_details, name="satisfactory_api_details"),
]