from rest_framework import serializers
from device.models import Device


class DeviceOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "name",
            "description",
            "serial_number",
            "number_of_rack_units",
            "electricity_consumption",
        )
