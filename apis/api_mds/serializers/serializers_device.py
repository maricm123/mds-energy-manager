from rest_framework import serializers
from device.models import Device
from django.shortcuts import get_object_or_404
from rack.models import Rack, RackUnit


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

    def validate(self, data):
        device = get_object_or_404(Device, id=data["device_id"])
        rack = get_object_or_404(Rack, id=data["rack_id"])

        if RackUnit.objects.device_already_exist_in_rack(device.id):
            raise serializers.ValidationError(
                {"device_id": "This device is already placed in a rack."}
            )

        data["device"] = device
        data["rack"] = rack
        data.pop("device_id", None)
        data.pop("rack_id", None)
        return data


class CreateDeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    serial_number = serializers.CharField(max_length=100)
    number_of_rack_units = serializers.IntegerField(min_value=1)
    electricity_consumption = serializers.IntegerField(min_value=1)


class DeviceSuggestionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    serial_number = serializers.CharField(max_length=100)
    number_of_rack_units = serializers.IntegerField(min_value=1)
    electricity_consumption = serializers.IntegerField(min_value=1)
