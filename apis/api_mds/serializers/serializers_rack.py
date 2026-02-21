from django.db.models import Sum
from rest_framework import serializers
from rack.models import Rack


class RackSerializer(serializers.ModelSerializer):
    total_units_used = serializers.SerializerMethodField(read_only=True)
    total_power_used = serializers.SerializerMethodField(read_only=True)
    total_power_used_display = serializers.SerializerMethodField(read_only=True)
    max_electricity_sustained_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rack
        fields = "__all__"

    def get_total_units_used(self, object):
        return object.devices.aggregate(
            total=Sum("number_of_rack_units")
        )["total"] or 0

    def get_total_power_used(self, object):
        return object.devices.aggregate(
            total=Sum("electricity_consumption")
        )["total"] or 0

    def get_total_power_used_display(self, object):
        value = self.get_total_power_used(object)
        return f"{value} W"

    def get_max_electricity_sustained_display(self, object):
        value = object.max_electricity_sustained
        return f"{value} W"


class CreateRackSerializer(serializers.Serializer):
    pass