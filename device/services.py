from typing import Any
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from device.models import Device
from rack.models import Rack, RackUnit
from rack.selectors import get_already_populated_units_for_given_rack
from rack.services import create_bulk_rack_units


def _find_first_free_block(*, populated_units: set[int], total_units: int, block_size: int) -> list[int] | None:
    latest_start = total_units - block_size + 1
    if latest_start < 1:
        return None

    for start in range(1, latest_start + 1):
        possible_units = list(range(start, start + block_size))
        if all(unit not in populated_units for unit in possible_units):
            return possible_units

    return None


def add_device_to_rack(*, device: Device, rack: Rack) -> list[int]:
    required_units = device.number_of_rack_units

    with transaction.atomic():
        rack = Rack.objects.select_for_update().get(id=rack.id)

        populated_units = get_already_populated_units_for_given_rack(rack_id=rack.id)

        free_block_for_device_units = _find_first_free_block(
            populated_units=populated_units,
            total_units=rack.total_units,
            block_size=required_units,
        )
        if free_block_for_device_units is None:
            raise ValidationError({"rack": "Rack does not have free units for this device."})

        existing_device_ids = RackUnit.objects.get_existing_devices(rack.id)

        existing_power = (
            Device.objects
            .filter(id__in=existing_device_ids)
            .aggregate(total=Coalesce(Sum("electricity_consumption"), 0))["total"]
        )

        if existing_power + device.electricity_consumption > rack.max_electricity_sustained:
            raise ValidationError({"rack": "Rack cannot handle this electricity consumption"})

        rack_unit_list = [
            RackUnit(rack_id=rack.id, device_id=device.id, unit=unit_number)
            for unit_number in free_block_for_device_units
        ]

        create_bulk_rack_units(rack_unit_list)

        return free_block_for_device_units


def create_device(device_data: dict[str, Any]) -> Device:
    try:
        with transaction.atomic():
            return Device.objects.create(**device_data)
    except IntegrityError:
        raise ValidationError({"serial_number": "Device with this serial number already exists."})
