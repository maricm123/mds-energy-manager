from collections import OrderedDict
from typing import Iterable
from apis.api_mds.serializers.serializers_device import DeviceOutputSerializer
from rack.models import RackUnit


def calculate_total_power_used_from_rack_units(rack_units: Iterable[RackUnit]) -> int:
    seen_device_ids: set[int] = set()
    total_power_used = 0

    for rack_unit in rack_units:
        device = rack_unit.device

        if device.id in seen_device_ids:
            continue

        seen_device_ids.add(device.id)
        total_power_used += device.electricity_consumption

    return total_power_used


def build_devices_with_units_from_rack_units(rack_units: Iterable[RackUnit]) -> list[dict]:
    grouped_by_device_id: "OrderedDict[int, dict]" = OrderedDict()

    for rack_unit in rack_units:
        device = rack_unit.device

        if device.id not in grouped_by_device_id:
            grouped_by_device_id[device.id] = {
                "device": DeviceOutputSerializer(device).data,
                "units": [],
            }

        grouped_by_device_id[device.id]["units"].append(rack_unit.unit)

    return list(grouped_by_device_id.values())
