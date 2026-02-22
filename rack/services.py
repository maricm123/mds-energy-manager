from django.db import transaction, IntegrityError
from rack.models import Rack
from django.core.exceptions import ValidationError
from typing import Any


def create_rack(rack_data: dict[str, Any]) -> Rack:
    try:
        with transaction.atomic():
            return Rack.objects.create(**rack_data)
    except IntegrityError:
        raise ValidationError({"serial_number": "Rack with this serial number already exists."})
