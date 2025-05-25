from django.db import models


class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=20)
    status = models.CharField(max_length=11, choices=[('installed', 'Installed'), ('uninstalled', 'Uninstalled')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
