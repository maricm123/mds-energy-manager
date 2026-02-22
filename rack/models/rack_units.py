from django.db import models
from django.db.models import CASCADE
from core.models.abstract_models import TimeStampable
from device.models import Device
from rack.models import Rack
from django.core.validators import MinValueValidator


class RackUnit(
    TimeStampable
):
    rack = models.ForeignKey(Rack, related_name="rack_units", on_delete=CASCADE)
    device = models.ForeignKey(Device, related_name="rack_units", on_delete=CASCADE)
    unit = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["rack", "unit"], name="unique_rack_unit"),
        ]
        ordering = ("rack", "unit")

    def __str__(self):
        return f"{self.rack} - {self.device} - {self.unit}"
