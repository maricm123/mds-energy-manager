from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from rack.models import Rack, RackUnit
from typing import Any
from rack.utils import (
    calculate_average_rack_energy,
    calculate_average_rack_units,
    calculate_power_utilization_percent
)
from django.utils import timezone


def create_rack(rack_data: dict[str, Any]) -> Rack:
    try:
        with transaction.atomic():
            return Rack.objects.create(**rack_data)
    except IntegrityError:
        raise ValidationError({"serial_number": "Rack with this serial number already exists."})


def create_bulk_rack_units(rack_unit_rows):
    try:
        RackUnit.objects.bulk_create(rack_unit_rows)
    except IntegrityError:
        raise ValidationError({"rack": "Error with device setting to rack"})


def rack_update(*, rack: Rack, data: dict) -> Rack:
    for key, value in data.items():
        setattr(rack, key, value)

    rack.save()
    return rack


def _can_store_device_in_rack(rack, device, used_units, used_energy):
    if used_units + device.number_of_rack_units > rack.total_units:
        return False

    if used_energy + device.electricity_consumption > rack.max_electricity_sustained:
        return False

    return True


def _calculate_extend_after_placement(
    racks,
    used_energy_by_rack,
    candidate_rack_id,
    device_energy,
):
    min_util = None
    max_util = None

    for rack in racks:
        new_used_energy = used_energy_by_rack[rack.id]

        if rack.id == candidate_rack_id:
            new_used_energy += device_energy

        util = calculate_power_utilization_percent(rack=rack, used_energy=new_used_energy)

        if min_util is None or util < min_util:
            min_util = util
        if max_util is None or util > max_util:
            max_util = util

    return max_util - min_util


def _choose_best_rack_for_device(*, racks, device, used_units_by_rack, used_energy_by_rack):
    current_best_rack = None
    best_extend = None

    for rack in racks:
        if not _can_store_device_in_rack(
            rack=rack,
            device=device,
            used_units=used_units_by_rack[rack.id],
            used_energy=used_energy_by_rack[rack.id]
        ):
            continue

        extend = _calculate_extend_after_placement(
            racks=racks,
            used_energy_by_rack=used_energy_by_rack,
            candidate_rack_id=rack.id,
            device_energy=device.electricity_consumption,
        )

        if best_extend is None or extend < best_extend:
            best_extend = extend
            current_best_rack = rack

    return current_best_rack


def suggest_algorithm_for_rack(racks, devices):
    ordered_devices = order_devices_per_power_and_units(racks, devices)

    used_energy_by_rack = {}
    used_units_by_rack = {}
    assigned_devices_by_rack = {}

    for rack in racks:
        used_energy_by_rack[rack.id] = 0
        used_units_by_rack[rack.id] = 0
        assigned_devices_by_rack[rack.id] = []

    unassigned_devices = []

    for device in ordered_devices:
        current_best_rack = _choose_best_rack_for_device(
            racks=racks,
            device=device,
            used_units_by_rack=used_units_by_rack,
            used_energy_by_rack=used_energy_by_rack,
        )

        if current_best_rack is None:
            unassigned_devices.append(device)
            continue

        used_energy_by_rack[current_best_rack.id] += device.electricity_consumption
        used_units_by_rack[current_best_rack.id] += device.number_of_rack_units
        assigned_devices_by_rack[current_best_rack.id].append(device)

    return assigned_devices_by_rack, used_energy_by_rack, used_units_by_rack, unassigned_devices


def order_devices_per_power_and_units(racks, devices):
    """
    Order devices per power and units based on rack situation
    """
    average_rack_max_energy = calculate_average_rack_energy(racks)
    average_rack_max_units = calculate_average_rack_units(racks)

    scored_devices = []

    for device in devices:
        w_ratio = device.electricity_consumption / average_rack_max_energy
        u_ratio = device.number_of_rack_units / average_rack_max_units

        score = (0.7 * w_ratio) + (0.3 * u_ratio)

        scored_devices.append((score, device))

    scored_devices.sort(key=lambda item: item[0], reverse=True)

    ordered_devices = []
    for score, device in scored_devices:
        ordered_devices.append(device)

    return ordered_devices


def build_suggestion_output(
        racks,
        assigned_devices_by_rack,
        used_energy_by_rack,
        used_units_by_rack,
        unassigned_devices
):
    racks_output = []

    for rack in racks:
        devices_for_rack = assigned_devices_by_rack.get(rack.id, [])

        serialized_devices = []
        for device in devices_for_rack:
            serialized_devices.append({
                "id": device.id,
                "name": device.name,
                "serial_number": device.serial_number,
                "electricity_consumption": device.electricity_consumption,
                "number_of_rack_units": device.number_of_rack_units,
            })

        total_power_used = used_energy_by_rack.get(rack.id, 0)
        units_used = used_units_by_rack.get(rack.id, 0)

        if rack.max_electricity_sustained > 0:
            power_utilization_percent = (total_power_used / rack.max_electricity_sustained) * 100
        else:
            power_utilization_percent = 0.0

        racks_output.append({
            "rack": rack,
            "devices": serialized_devices,
            "total_power_used": total_power_used,
            "power_utilization_percent": power_utilization_percent,
            "units_used": units_used,
        })

    serialized_unassigned = []
    for device in unassigned_devices:
        serialized_unassigned.append({
            "id": device.id,
            "name": device.name,
            "serial_number": device.serial_number,
            "electricity_consumption": device.electricity_consumption,
            "number_of_rack_units": device.number_of_rack_units,
        })

    return {
        "racks": racks_output,
        "unassigned_devices": serialized_unassigned,
    }


@transaction.atomic
def delete_rack(rack):
    RackUnit.objects.delete_rack(rack_id=rack.id)

    rack.deleted_at = timezone.now()
    rack.save(update_fields=["deleted_at"])
