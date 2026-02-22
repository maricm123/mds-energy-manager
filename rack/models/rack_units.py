from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE
from core.models.abstract_models import TimeStampable
from device.models import Device
from rack.models import Rack
from django.core.validators import MinValueValidator


class RackUnitQuerySet(models.QuerySet):
    def device_already_exist_in_rack(self, device_id):
        return self.filter(device_id=device_id).exists()

    def get_existing_devices(self, rack_id):
        return self.filter(rack_id=rack_id).values_list("device_id", flat=True).distinct()


class RackUnitManager(models.Manager.from_queryset(RackUnitQuerySet)):
    pass


class RackUnit(
    TimeStampable
):
    rack = models.ForeignKey(Rack, related_name="rack_units", on_delete=CASCADE)
    device = models.ForeignKey(Device, related_name="rack_units", on_delete=CASCADE)
    unit = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    objects = RackUnitManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["rack", "unit"], name="unique_rack_unit"),
        ]
        ordering = ("rack", "unit")

    def __str__(self):
        return f"{self.rack} - {self.device} - {self.unit}"

    def clean(self):
        """
        Validation mostly for admin dashboard
        """
        super().clean()

        if not self.rack or not self.device:
            return

        if self.unit and self.rack.total_units and self.unit > self.rack.total_units:
            raise ValidationError({"unit": "Unit exceeds rack total units."})

        already_populated_units = self.__class__.objects.filter(rack_id=self.rack.id, device_id=self.device.id)

        if self.id:
            already_populated_units = already_populated_units.exclude(id=self.id)

        current_count = already_populated_units.count()

        if current_count >= self.device.number_of_rack_units:
            raise ValidationError(
                {"device": "This device already have maximum number of rack units in this rack."}
            )
