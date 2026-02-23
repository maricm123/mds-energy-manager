from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from rack.models import Rack, RackUnit
from typing import Any


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


def suggest_algorithm_for_rack(racks, devices):
    print(racks)
    print(devices)
# nadji najzahtevnije uredjaje (energy consumption i koliko jedinica zauzimaju)


def order_devices_per_power_and_units(racks, devices):
    """
    Order devices per power and units based on rack situation
    """
    calculate_average_rack_max_energy
    calculate_average_rack_max_units