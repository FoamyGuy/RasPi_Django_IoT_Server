from django.contrib import admin

from apps.iot_server.models import DataSource, DataValue

# Register your models here.
admin.site.register(DataSource)
admin.site.register(DataValue)