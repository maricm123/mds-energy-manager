from rest_framework import serializers
from apis.utils import (
    build_devices_with_units_from_rack_units,
    calculate_total_power_used_from_rack_units
)
from rack.models import Rack


class RackSerializer(serializers.ModelSerializer):
    total_units_used = serializers.SerializerMethodField(read_only=True)
    total_power_used = serializers.SerializerMethodField(read_only=True)
    total_power_used_display = serializers.SerializerMethodField(read_only=True)
    max_electricity_sustained_display = serializers.SerializerMethodField(read_only=True)
    devices = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rack
        fields = "__all__"

    def get_total_units_used(self, object):
        return object.rack_units.count()

    def get_total_power_used(self, object):
        return calculate_total_power_used_from_rack_units(object.rack_units.all())

    def get_devices(self, object):
        return build_devices_with_units_from_rack_units(object.rack_units.all())

    def get_total_power_used_display(self, object):
        return f"{self.get_total_power_used(object)} W"

    def get_max_electricity_sustained_display(self, object):
        value = object.max_electricity_sustained
        return f"{value} W"


class CreateRackSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    serial_number = serializers.CharField(max_length=100)
    total_units = serializers.IntegerField(min_value=1)
    max_electricity_sustained = serializers.IntegerField(min_value=1)
