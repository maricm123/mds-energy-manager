from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from rack.models import Rack, RackUnit


def get_rack_with_device_units(*, rack_id: int) -> Rack:
    # TODO: move queries to model manager
    rack_units_qs = RackUnit.objects.select_related("device").order_by("unit")

    return (
        Rack.objects
        .prefetch_related(Prefetch("rack_units", queryset=rack_units_qs))
        .get(id=rack_id)
    )


def get_already_populated_units_for_given_rack(rack_id):
    return set(
        RackUnit.objects
        .filter(rack_id=rack_id)
        .values_list("unit", flat=True)
    )


def get_racks_from_list(rack_list):
    racks_by_id = Rack.objects.in_bulk(rack_list)

    missing_ids = []
    for rack_id in rack_list:
        if rack_id not in racks_by_id:
            missing_ids.append(rack_id)

    if missing_ids:
        raise ValidationError({"rack_ids": f"Racks not found: {missing_ids}"})

    ordered_racks = []
    for rack_id in rack_list:
        ordered_racks.append(racks_by_id[rack_id])

    return ordered_racks
