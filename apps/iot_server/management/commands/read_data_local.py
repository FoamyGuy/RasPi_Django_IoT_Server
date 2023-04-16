from django.core.management import BaseCommand
import board
import adafruit_ahtx0

from apps.iot_server.models import DataValue, DataSource


class Command(BaseCommand):
    help = "Read a data value from local sensor"
    def handle(self, *args, **options):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        sensor = adafruit_ahtx0.AHTx0(i2c)

        source = DataSource.objects.get(name="Local AHT20")
        temperature_reading = DataValue(source=source, user=source.user)
        temperature_reading.value = {
            "type": "temperature",
            "value": sensor.temperature,
            "unit": "C"
        }
        temperature_reading.save()

        humidity_reading = DataValue(source=source, user=source.user)
        humidity_reading.value = {
            "type": "humidity",
            "value": sensor.relative_humidity,
            "unit": "%"
        }
        humidity_reading.save()