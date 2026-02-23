from django.core.exceptions import ValidationError
from device.models import Device


def get_devices_from_list(device_list):
    devices_by_id = Device.objects.in_bulk(device_list)

    missing_ids = []
    for device_id in device_list:
        if device_id not in devices_by_id:
            missing_ids.append(device_id)

    if missing_ids:
        raise ValidationError({"device_ids": f"Devices not found: {missing_ids}"})

    ordered_devices = []
    for device_id in device_list:
        ordered_devices.append(devices_by_id[device_id])

    return ordered_devices
