from django.db.models import Prefetch
from rack.models import Rack, RackUnit


def get_rack_with_device_units(*, rack_id: int) -> Rack:
    rack_units_qs = RackUnit.objects.select_related("device").order_by("unit")

    return (
        Rack.objects
        .prefetch_related(Prefetch("rack_units", queryset=rack_units_qs))
        .get(id=rack_id)
    )
