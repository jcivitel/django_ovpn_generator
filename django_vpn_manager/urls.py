from django.urls import path
from . import views

urlpatterns = [
    path("create-vpn-server/", views.create_vpn_server, name="create_vpn_server"),
    path(
        "create-client-profile/",
        views.create_client_profile,
        name="create_client_profile",
    ),
    path(
        "download-client-config/<int:profile_id>/",
        views.download_client_config,
        name="download_client_config",
    ),
]
