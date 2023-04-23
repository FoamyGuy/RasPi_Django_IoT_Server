import secrets

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from encrypted_fields import fields
from core.settings import HASH_KEY


# Create your models here.


def init_api_token_str():
    token = secrets.token_urlsafe(64)
    while DataSource.objects.filter(token=token).count() > 0:
        token = secrets.token_urlsafe(64)
    return token


class DataSource(models.Model):
    name = models.CharField("Name", max_length=128, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField("Created At", default=timezone.now)
    local = models.BooleanField("Local", default=True)
    _token_data = fields.EncryptedCharField(max_length=512, default=init_api_token_str, null=False)
    token = fields.SearchField(hash_key=HASH_KEY, encrypted_field_name="_token_data")

    activated = models.BooleanField("Activated", default=False)
    def __str__(self):
        return f"{self.user.username} - {self.name}"

    @property
    def value_count(self):
        return DataValue.objects.filter(source=self).count()


class DataValue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=False, blank=False)
    """
    {
        "type": "temperature"
        "value": 23.3
        "unit": "C"
    }
    """
    value = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.created_at} - {self.user} - {self.source.name} - {self.value['value']} {self.value['unit']}"


