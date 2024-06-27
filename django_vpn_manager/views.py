import io
import zipfile

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import VPNServerForm, ClientProfileForm
from .models import ClientProfile
from .utils import generate_server_certificates, generate_client_certificates


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def create_vpn_server(request):
    if request.method == "POST":
        form = VPNServerForm(request.POST)
        if form.is_valid():
            try:
                server = form.save(commit=False)
                certificates = generate_server_certificates(server.name)
                server.ca_certificate = certificates["ca_cert"]
                server.server_certificate = certificates["server_cert"]
                server.server_key = certificates["server_key"]
                server.dh_params = certificates["dh_params"]
                server.save()
                messages.success(request, "VPN-Server erfolgreich erstellt.")
                return redirect("admin:index")
            except Exception as e:
                messages.error(
                    request, f"Fehler beim Erstellen des VPN-Servers: {str(e)}"
                )
    else:
        form = VPNServerForm()
    return render(request, "create_vpn_server.html", {"form": form})


@user_passes_test(is_superuser)
def create_client_profile(request):
    if request.method == "POST":
        form = ClientProfileForm(request.POST)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                server = profile.server
                certificates = generate_client_certificates(
                    profile.name, server.ca_certificate, server.server_key
                )
                profile.client_certificate = certificates["client_cert"]
                profile.client_key = certificates["client_key"]
                profile.save()
                messages.success(request, "Client-Profil erfolgreich erstellt.")
                return redirect("admin:index")
            except Exception as e:
                messages.error(
                    request, f"Fehler beim Erstellen des Client-Profils: {str(e)}"
                )
    else:
        form = ClientProfileForm()
    return render(request, "create_client_profile.html", {"form": form})


@user_passes_test(is_superuser)
def download_client_config(request, profile_id):
    try:
        profile = ClientProfile.objects.get(id=profile_id)
        server = profile.server

        config = f"""client
dev tun
proto udp
remote {server.ip_address} {server.port}
resolv-retry infinite
nobind
persist-key
persist-tun
ca [inline]
cert [inline]
key [inline]
remote-cert-tls server
cipher AES-256-CBC
verb 3

<ca>
{server.ca_certificate}
</ca>

<cert>
{profile.client_certificate}
</cert>

<key>
{profile.client_key}
</key>
"""

        # Erstellen eines ZIP-Archivs mit der Konfigurationsdatei
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{profile.name}.ovpn", config)

        # Rücksetzen des Puffers für die Antwort
        zip_buffer.seek(0)

        # Senden der ZIP-Datei als Antwort
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = (
            f'attachment; filename="{profile.name}_config.zip"'
        )
        return response

    except ClientProfile.DoesNotExist:
        messages.error(request, "Client-Profil nicht gefunden.")
        return redirect("admin:index")
    except Exception as e:
        messages.error(
            request, f"Fehler beim Herunterladen der Konfiguration: {str(e)}"
        )
        return redirect("admin:index")
