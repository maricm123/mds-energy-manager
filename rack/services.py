from django.db import transaction, IntegrityError
from rack.models import Rack, RackUnit
from django.core.exceptions import ValidationError
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
    pass
