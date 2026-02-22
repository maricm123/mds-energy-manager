from rest_framework import serializers

from device.models import Device


class DeviceOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ("rack", )
