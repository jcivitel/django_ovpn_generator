from django.contrib import admin
from .models import VPNServer, ClientProfile


@admin.register(VPNServer)
class VPNServerAdmin(admin.ModelAdmin):
    list_display = ("name", "ip_address", "port")
    search_fields = ("name", "ip_address")


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "server")
    list_filter = ("server",)
    search_fields = ("user__username", "name")
