from typing import Any
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from device.models import Device


def create_device(device_data: dict[str, Any]) -> Device:
    try:
        with transaction.atomic():
            return Device.objects.create(**device_data)
    except IntegrityError:
        raise ValidationError({"serial_number": "Device with this serial number already exists."})
