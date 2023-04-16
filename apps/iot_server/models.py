from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class DataSource(models.Model):
    name = models.CharField("Name", max_length=128, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField("Created At", default=timezone.now)
    local = models.BooleanField("Local", default=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


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
