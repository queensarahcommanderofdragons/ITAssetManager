from django.urls import path
from . import views
from .views import asset_list, asset_detail, asset_create, asset_update, asset_delete, export_assets_csv, user_assets, user_list, user_create, user_edit, user_delete

urlpatterns = [
    path("", asset_list, name="asset_list"),
    path("new/", asset_create, name="asset_create"),
    path("<int:pk>/edit/", asset_update, name="asset_update"),
    path("<int:pk>/delete/", asset_delete, name="asset_delete"),
    path("export/csv/", export_assets_csv, name="export_assets_csv"),
    path("assets/<int:pk>/", asset_detail, name="asset_detail"),
    path("users/", user_list, name="user_list"),
    path("users/new/", user_create, name="user_create"),
    path("users/<str:username>/edit/", user_edit, name="user_edit"),
    path("users/<str:username>/delete/", user_delete, name="user_delete"),
    path("users/<str:username>/assets/", user_assets, name="user_assets"),
]

