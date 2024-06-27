from django import forms
from .models import VPNServer, ClientProfile


class VPNServerForm(forms.ModelForm):
    class Meta:
        model = VPNServer
        fields = ["name", "ip_address", "port"]


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ["user", "name", "server"]
