from rest_framework import serializers
from device.models import Device
from django.shortcuts import get_object_or_404
from rack.models import Rack


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


class AddDeviceToRackSerializer(serializers.Serializer):
    device_id = serializers.IntegerField(min_value=1, required=True)
    rack_id = serializers.IntegerField(min_value=1, required=True)

    def validate_device_id(self, value):
        device = get_object_or_404(Device, id=value)
        return device

    def validate_rack_id(self, value):
        rack = get_object_or_404(Rack, id=value)
        return rack


class CreateDeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    serial_number = serializers.CharField(max_length=100)
    number_of_rack_units = serializers.IntegerField(min_value=1)
    electricity_consumption = serializers.IntegerField(min_value=1)
