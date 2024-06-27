from django.db import models
from django.contrib.auth.models import User


class VPNServer(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    ca_certificate = models.TextField()
    server_certificate = models.TextField()
    server_key = models.TextField()
    dh_params = models.TextField()

    def __str__(self):
        return self.name


class ClientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    server = models.ForeignKey(VPNServer, on_delete=models.CASCADE)
    client_certificate = models.TextField()
    client_key = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.name}"
