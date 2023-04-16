from django.core.management import BaseCommand
from apps.iot_server.models import DataValue, DataSource


class Command(BaseCommand):
    help = "Read a data value from local sensor"
    def handle(self, *args, **options):
        source = DataSource.objects.get(name="Local AHT20")
        temperature_reading = DataValue(source=source, user=source.user)
        temperature_reading.value = {
            "type": "temperature",
            "value": 23.3,
            "unit": "C"
        }
        temperature_reading.save()

        humidity_reading = DataValue(source=source, user=source.user)
        humidity_reading.value = {
            "type": "humidity",
            "value": 30.2,
            "unit": "%"
        }
        humidity_reading.save()